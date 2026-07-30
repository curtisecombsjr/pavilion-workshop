"""Result logger plugin that records test completion via saLog.

For each completed test, calls:
    saLog -n <node>,<node>,... -c <comment> -u <user> -a <action>

Nodes are taken from the keys of results['per_file'], which are the
normalized hostnames written by the per_file: name result parser.

Example pavilion.yaml entry:
    result_loggers:
      - plugin: sa_log
        action: released
        salog_path: /home/pavilion/pavilion2/saLog
"""

import io
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, TextIO

from pavilion import output
from pavilion.errors import ResultLoggerPluginError
from pavilion.result_logging.base_classes import ResultLoggerPlugin, ResultLogger


class SaLogLoggerFactory(ResultLoggerPlugin):
    """Factory plugin for the 'sa_log' result logger."""

    def __init__(self):
        super().__init__(
            name='sa_log',
            description='Log test results via the saLog command, one call per test run.',
            priority=self.PRIO_COMMON,
        )

    def validate_config(self, config: Dict) -> None:
        if config.get('plugin', '') != self.name:
            raise ResultLoggerPluginError(
                "Name {} does not match plugin type {}.".format(
                    config.get('plugin'), self.name))

        salog_path = config.get('salog_path', 'saLog')
        path = Path(salog_path)
        if path.is_absolute() and not path.exists():
            raise ResultLoggerPluginError(
                "sa_log: salog_path '{}' does not exist.".format(salog_path))

    def _make_logger(self,
                     config: Dict,
                     sid: str,
                     outfile: Optional[TextIO] = None) -> 'SaLogResultLogger':
        return SaLogResultLogger(
            salog_path=config.get('salog_path', 'saLog'),
            action=config.get('action', 'released'),
            outfile=outfile,
        )


class SaLogResultLogger(ResultLogger):
    """Calls saLog once per test result to record node usage."""

    def __init__(self, salog_path: str, action: str,
                 outfile: Optional[TextIO] = None):
        self.salog_path = salog_path
        self.action = action
        self.outfile = outfile or io.StringIO()

    def log(self, results: Dict) -> None:
        nodes = self._nodes_from_results(results)
        if not nodes:
            output.fprint(
                self.outfile,
                "sa_log: no node data (file/per_file) for '{}', skipping saLog call."
                .format(results.get('name', '?')))
            return

        node_str = ','.join(nodes)
        test_name = results.get('name', 'unknown')
        result = results.get('result', 'UNKNOWN')
        user = results.get('user', '')
        comment = "{} result={}".format(test_name, result)

        cmd = [self.salog_path,
               '-n', node_str,
               '-c', comment,
               '-a', self.action]
        if user:
            cmd += ['-u', user]

        output.fprint(
            self.outfile,
            "sa_log: running: {}".format(' '.join(cmd)))

        try:
            proc = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if proc.stdout:
                output.fprint(self.outfile, proc.stdout.decode().rstrip())
        except FileNotFoundError:
            output.fprint(
                self.outfile,
                "sa_log: saLog binary not found at '{}'. Skipping.".format(
                    self.salog_path))
        except subprocess.CalledProcessError as err:
            output.fprint(
                self.outfile,
                "sa_log: saLog exited {} for '{}': {}".format(
                    err.returncode, test_name, err.stderr.decode().rstrip()))

    @staticmethod
    def _nodes_from_results(results: Dict) -> List[str]:
        """Return the list of hostnames the test ran on.

        Handles both result shapes:
        - flatten_results: True (Pavilion flattens per_file into one record per
          node, deletes 'per_file', and puts the node name in 'file').
        - flatten_results: False (unflattened 'per_file' dict keyed by node).
        """
        # Flattened form: one record per node, node name in 'file'.
        node = results.get('file')
        if node:
            return [node]
        # Unflattened form: per_file is a dict keyed by node hostname.
        per_file = results.get('per_file')
        if isinstance(per_file, dict):
            return sorted(per_file.keys())
        return []
