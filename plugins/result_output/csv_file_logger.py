"""CSV file result logger plugin.

Logs test results to a CSV file, appending one row per test run.

Configuration keys (all values are strings in pavilion.yaml):
    plugin      (required) Must be "csv_file".
    dest        (required) Absolute path to the CSV file, or to a directory
                           (file will be named "results.csv" inside it).
    per_series  (optional) "true" to write one CSV file per series, named
                           "<sid>.csv" inside dest (which must be a directory).
    columns     (optional) Comma-separated list of result keys to include as
                           dedicated columns.  Defaults to all BASE_RESULTS
                           fields.  Any result key NOT in this list is
                           JSON-serialized into an "extra" column.

Example pavilion.yaml entry:
    result_loggers:
      - plugin: csv_file
        dest: /home/pavilion/logs/results
        per_series: "true"
"""

import csv
import io
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, TextIO

from pavilion import output
from pavilion.errors import ResultLoggerPluginError
from pavilion.lockfile import FuzzyLock
from pavilion.result_logging.base_classes import ResultLoggerPlugin, ResultLogger


# Scalar BASE_RESULTS fields — get their own CSV columns.
_SCALAR_FIELDS = [
    'name',
    'id',
    'result',
    'sys_name',
    'user',
    'created',
    'started',
    'finished',
    'duration',
    'return_value',
    'test_version',
    'pav_version',
]

# Nested/complex BASE_RESULTS fields — serialized as JSON strings in their
# own column so they are still retrievable but don't explode the column count.
_NESTED_FIELDS = [
    'sched',
    'var',
    'job_info',
    'permute_on',
    'pav_result_errors',
    'per_file',
]

# All known BASE_RESULTS columns in display order.
DEFAULT_COLUMNS = _SCALAR_FIELDS + _NESTED_FIELDS


class CsvFileLoggerFactory(ResultLoggerPlugin):
    """Factory plugin for the 'csv_file' result logger."""

    def __init__(self):
        super().__init__(
            name='csv_file',
            description='Log test results to a CSV file, one row per test run.',
            priority=self.PRIO_COMMON,
        )

    def validate_config(self, config: Dict) -> None:
        plugin_name = config.get('plugin', '')
        dest = config.get('dest')

        if plugin_name != self.name:
            raise ResultLoggerPluginError(
                "Name {} does not match plugin type {}.".format(
                    plugin_name, self.name))

        if dest is None:
            raise ResultLoggerPluginError(
                "csv_file logger requires a 'dest' path.")

        if not Path(dest).is_absolute():
            raise ResultLoggerPluginError(
                "csv_file 'dest' must be an absolute path; got: {}".format(dest))

    def _make_logger(self,
                     config: Dict,
                     sid: str,
                     outfile: Optional[TextIO] = None) -> 'CsvFileResultLogger':
        dest = Path(config.get('dest'))

        per_series = config.get('per_series', '').strip().lower() in (
            'true', '1', 'yes')

        if per_series:
            # One CSV file per series inside dest directory.
            dest.mkdir(parents=True, exist_ok=True)
            dest = dest / '{}.csv'.format(sid)
        elif dest.suffix != '.csv':
            # dest is a directory; use a fixed filename inside it.
            dest.mkdir(parents=True, exist_ok=True)
            dest = dest / 'results.csv'

        # Optional column override: comma-separated list of result keys.
        columns_cfg = config.get('columns', '').strip()
        if columns_cfg:
            columns = [c.strip() for c in columns_cfg.split(',') if c.strip()]
        else:
            columns = list(DEFAULT_COLUMNS)

        return CsvFileResultLogger(dest, columns, outfile)


class CsvFileResultLogger(ResultLogger):
    """Appends one CSV row per test result to a shared file.

    Known columns are written as individual fields.  Any result key that is
    not in the configured column list is JSON-serialized into an 'extra'
    column so no data is lost.  The header row is written once when the file
    is first created (or is empty).  FuzzyLock prevents concurrent writes
    from corrupting the file.
    """

    def __init__(self, dest: Path, columns: List[str],
                 outfile: Optional[TextIO] = None):
        self.dest = dest
        # Always end with 'extra' to capture any user-defined result keys.
        self.columns = columns
        self.all_columns = columns + ['extra']
        self.outfile = outfile or io.StringIO()

    def log(self, results: Dict) -> None:
        output.fprint(
            self.outfile,
            "{}: Logging {} ({}) to {}...".format(
                type(self).__name__,
                results.get('name', '?'),
                results.get('result', '?'),
                self.dest))

        self.dest.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.dest.parent / (self.dest.name + '.lock')

        with FuzzyLock(lock_path, timeout=10):
            write_header = (
                not self.dest.exists() or self.dest.stat().st_size == 0)

            # Collect keys not covered by the defined columns.
            known = set(self.columns)
            extra_data = {k: v for k, v in results.items() if k not in known}

            # Build the row dict.
            row = {}
            for col in self.columns:
                val = results.get(col)
                if isinstance(val, (dict, list)):
                    row[col] = json.dumps(val, default=str)
                elif val is None:
                    row[col] = ''
                else:
                    row[col] = str(val)

            row['extra'] = json.dumps(extra_data, default=str) if extra_data else ''

            with open(str(self.dest), 'a', newline='') as fout:
                writer = csv.DictWriter(fout, fieldnames=self.all_columns)
                if write_header:
                    writer.writeheader()
                writer.writerow(row)

        self._syslog(results)

    def _syslog(self, results: Dict) -> None:
        result = results.get('result', '')
        priority = 'user.info' if result == 'PASS' else 'user.err'
        message = 'id={} name={} result={}'.format(
            results.get('id', '?'),
            results.get('name', '?'),
            result or '?',
        )
        try:
            subprocess.run(
                ['logger', '-t', 'pavilion', '-p', priority, message],
                check=True,
            )
        except (OSError, subprocess.CalledProcessError) as err:
            output.fprint(self.outfile,
                          "csv_file logger: syslog failed: {}".format(err))
