# Run-of-show — Pavilion workshop demos

Everything below is **verified working** on the cluster (2026-07-26). Nine demos, each a
one-command script. The deck (`../pavilion-workshop.pptx`) has a slide + speaker notes per demo.

## Before you start (once, at the podium)

```bash
ssh root@pbs-server           # keyed, no password
sudo -iu pavilion             # pav config lives in pavilion's home — the -i matters
cd ~/pav_demo                 # the demo scripts are deployed here

# For L9 only — export the OpenSearch password into your shell (never hard-code it):
export OS_PASS='<your OpenSearch password>'
```

Tips:
- Every script prints the command in cyan, then the real `pav` output.
- Scripts pause between steps; press **enter** to advance. `NOPAUSE=1 ./01-basic.sh` to skip pauses.
- `pav --quiet …` (used in the scripts) hides a harmless config-label warning.

## The ladder

| # | Script | Shows | One-liner if you'd rather type it |
|---|--------|-------|-----------------------------------|
| L1 | `./01-basic.sh` | PASS + intentional FAIL (raw) | `pav run demo_echo.demo_pass_raw demo_echo.demo_fail_raw` |
| L2 | `./02-metrics.sh` | result parsing → numbers | `pav run demo_echo.demo_metrics` then `pav results --full <sid>` |
| L3 | `./03-permutations.sh` | 1 config → 6 tests | `pav run demo_perms.matrix` |
| L4 | `./04-pbs.sh` | PBS submit; **running** in pav + PBS; result | `pav run demo_echo.demo_pass_pbs` → `pav status <sid>` + `qstat -a` → `pav results <sid>` |
| L5 | `./05-modes.sh` | mode overrides a var | `pav run -m prod demo_modes.mode_demo` |
| L6 | `./06-series.sh` | run a group | `pav series run demo_series` |
| L7 | `./07-command-plugins.sh` | your command plugins | `pav hello` / `pav recent` / `pav test-summary` / `pav disk-usage` |
| L8 | `./08-output-csv.sh` | csv_file logger | `tail /home/pavilion/pav_logs/results.csv` |
| L9 | `./09-opensearch.sh` | opensearch logger → index → Grafana | `pav run opensearch_verify` then `python3 ~/opensearch_results.py --name opensearch_verify` |
| L10 | `./10-mysql.sh` | mysql logger → MySQL table | `pav run demo_echo.demo_metrics` then `mysql pavilion -e "SELECT pav_id,name,result,ROUND(duration,3) dur FROM results ORDER BY logged_at DESC LIMIT 5"` |

Then open **Grafana**: `http://<your-grafana-host>:3000`.

## Gotchas / fallbacks

- **L4 (PBS) timing:** run `pav run …` then *immediately* `qstat -a` to catch the job before it finishes.
- **L6 (series):** uses `ordered: False` on purpose — ordered series need a background manager and can stall.
- **L9:** if `OS_PASS` isn't set, the query errors. The 08-output-csv demo is a safe fallback if OpenSearch is unhappy.
- **L10 (MySQL):** MariaDB must be running on pbs-server (`systemctl status mariadb`). The `mysql` CLI as the `pavilion` user auths via unix_socket (no password). The logger is **non-fatal** — if MySQL is down, other demos still pass (results just skip the MySQL row).
- **⚠️ Do NOT display `pavilion.yaml` on screen** — it contains a plaintext OpenSearch password. Use the deck's redacted version.
- Nothing is destructive; re-running demos just adds more runs (which makes `recent`/`test-summary` richer).

## Where things live

- Demo scripts: `~/pav_demo/` on **pbs-server** (source of truth: `hpc/pavilion-presentation/demo/`).
- Test/mode/series configs I authored: `hpc/pavilion-presentation/configs/` (deployed into `/home/pavilion/pavilion2/config/{suites,modes,series}`).
- Command plugins (fixed): `/home/pavilion/pavilion2/config/plugins/command/` (source: `hpc/pavilion2/config/plugins/command/`).
- The deck + its build script: `hpc/pavilion-presentation/pavilion-workshop.pptx`, `build_deck.py`.
