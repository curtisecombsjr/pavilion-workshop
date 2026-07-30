# plugins/

The custom Pavilion plugins demoed in this workshop. Each plugin is a `.py` file plus a
matching `.yapsy-plugin` file (that extension — **not** `.plugin` — is what makes Pavilion
discover it). Two kinds, in two subdirs that mirror the cluster layout:

```
plugins/
├── result_output/   → deploy to ~/pavilion2/config/plugins/result_output/
└── command/         → deploy to ~/pavilion2/config/plugins/command/
```

## Result loggers (`result_output/`)

Run at the end of the results stage; configured once in `pavilion.yaml` under `result_loggers:`.

| Plugin | What it does |
|--------|--------------|
| `csv_file_logger` | Appends one CSV row per test (result, duration, parsed metrics, permute vars). |
| `sa_log_logger` | NASA/NOAA `saLog` logger — one CSV row per node on release. Reads the node from the flattened `file` field (works with `flatten_results: True`). |
| `opensearch_logger` | Indexes each result document into OpenSearch (`pavilion-results`). Takes host/port/index/user/**password** from `pavilion.yaml` — no secret is hard-coded here. |
| `mysql_logger` | Writes one row per result into MySQL/MariaDB. **Passwordless** via the local unix_socket auth plugin (no credentials in `pavilion.yaml`). Needs `pymysql`. |

All are **non-fatal**: if the destination is down, the logger warns and skips the row; the test still passes.

Example `pavilion.yaml`:

```yaml
result_loggers:
  - plugin: csv_file
    path: /home/pavilion/pav_logs/results.csv
  - plugin: sa_log
    action: released
    salog_path: /home/pavilion/pavilion2/saLog
  - plugin: opensearch
    host: 10.200.0.254
    index: pavilion-results
    # username / password …
  - plugin: mysql
    database: pavilion
    table: results
    unix_socket: /var/lib/mysql/mysql.sock
```

## Command plugins (`command/`)

Add new `pav <command>` subcommands; Pavilion auto-discovers them (no `pavilion.yaml` entry needed).

| Plugin | Adds |
|--------|------|
| `hello` | A friendly sanity check + Pavilion info. |
| `recent` | The most recent test runs, colored by result. |
| `test_summary` | A PASS/FAIL tally across recent runs. |
| `disk_usage` | Space consumed by test runs / builds / series. |

## Deploying

Copy the `.py` + `.yapsy-plugin` into the matching cluster dir and Pavilion picks them up:

```bash
scp result_output/*  root@pbs-server:/tmp/ && \
  ssh root@pbs-server 'sudo -u pavilion cp /tmp/*_logger.*  ~pavilion/pavilion2/config/plugins/result_output/'
scp command/*  root@pbs-server:/tmp/ && \
  ssh root@pbs-server 'sudo -u pavilion cp /tmp/{hello,recent,test_summary,disk_usage}.*  ~pavilion/pavilion2/config/plugins/command/'
# clear stale bytecode if replacing: rm the plugin dir's __pycache__/*.pyc
```

> Source-of-truth note: the result loggers are also maintained standalone at
> `github.com/curtisecombsjr/result_loggers`; the command plugins come from the Pavilion
> framework project. The copies here are the versions shown in the workshop.
