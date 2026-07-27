# plugins/

Custom Pavilion plugins written for this workshop.

## MySQL result logger

`mysql_logger.py` + `mysql_logger.yapsy-plugin` — a **result logger** that writes one row per test
result into a MySQL/MariaDB table.

- **Passwordless:** connects over the local unix socket, authenticating via MariaDB's
  `unix_socket` auth plugin — so **no credentials live in `pavilion.yaml`**.
- **Non-fatal:** if the database is down, the logger warns and skips the row; the test still passes.
- **Deploys to:** `~/pavilion2/config/plugins/result_output/` on the cluster. A `.yapsy-plugin`
  file (not `.plugin`) next to the `.py` is what makes Pavilion discover it.
- **Requires:** `pymysql` (see `../requirements.txt`).

Example `pavilion.yaml` entry:

```yaml
result_loggers:
  - plugin: mysql
    database: pavilion
    table: results
    unix_socket: /var/lib/mysql/mysql.sock
```

## The other plugins shown in the workshop

The command plugins (`hello`, `recent`, `test-summary`, `disk-usage`) and the other result loggers
(`csv_file`, `saLog`, `opensearch`) demoed in the deck live with the framework project, not here:

- Source of truth: **`../../pavilion2/`** (the Pavilion framework project on this machine).
- On the cluster: `~/pavilion2/config/plugins/{command,result_output}/`.

They're referenced from the demo scripts (`07-command-plugins.sh`, `08-output-csv.sh`,
`09-opensearch.sh`, `12-salog.sh`) but kept in the framework repo to avoid divergence.
