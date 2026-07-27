# Run-of-show — Pavilion workshop demos

Everything below is **verified working** on the cluster (2026-07-26). Each demo is a
one-command script; every `pav run` goes through PBS and is followed by `qstat -a`.
The deck (`../deck/pavilion-workshop.pptx`) has a slide + speaker notes per demo.

## Before you start (once, at the podium)

```bash
ssh root@pbs-server           # keyed, no password
sudo -iu pavilion             # pav config lives in pavilion's home — the -i matters
cd ~/pav_demo                 # the demo scripts are deployed here
```

No credentials to set up: L9's read-back (`opensearch_results.py`) auto-loads the OpenSearch
password from `pavilion.yaml` (the same place the logger reads it). Set `OS_PASS` only if you
want to override it.

Tips:
- Every script prints the command in cyan, then the real `pav` output.
- Scripts pause between steps; press **enter** to advance. `NOPAUSE=1 ./01-basic.sh` to skip pauses.
- `pav --quiet …` (used in the scripts) hides a harmless config-label warning.

## The ladder

Every `pav run` below is a **PBS job** — each demo does `pav run …` then `qstat -a` to prove the
scheduler dispatched it. (Running a PBS test also proves PBS itself works.)

| # | Script | Shows | One-liner if you'd rather type it |
|---|--------|-------|-----------------------------------|
| Inherit | `./00-inheritance.sh` | inherits_from: child inherits base, overrides its delta | `pav run demo_inherit.small demo_inherit.large demo_inherit.debug` → `qstat -a` → `pav results --full <sid>` |
| L1 | `./01-basic.sh` | PASS + intentional FAIL (PBS) | `pav run demo_pbs.pass demo_pbs.fail` → `qstat -a` |
| L2 | `./02-metrics.sh` | result parsing → numbers | `pav run demo_pbs.metrics` → `qstat -a` → `pav results --full <sid>` |
| L3 | `./03-permutations.sh` | 1 config → 6 PBS tests | `pav run demo_perms.matrix` → `qstat -a` |
| L4 | `./04-pbs.sh` | PBS submit; **running** in pav + PBS; result | `pav run demo_pbs.pass` → `pav status <sid>` + `qstat -a` → `pav results <sid>` |
| L5 | `./05-modes.sh` | mode flips FAIL→PASS (throughput 1200→1400 vs a >1300 check) | `pav run demo_modes.mode_demo` (FAIL) → `pav run -m prod demo_modes.mode_demo` (PASS) → `qstat -a` |
| L6 | `./06-series.sh` | run a group (one PBS job per set) | `pav series run demo_series` → `qstat -a` |
| L7 | `./07-command-plugins.sh` | your command plugins | `pav hello` / `pav recent` / `pav test-summary` / `pav disk-usage` |
| L8 | `./08-output-csv.sh` | csv_file logger | `pav run demo_pbs.pass demo_pbs.metrics` → `qstat -a` → `tail ~/pav_logs/results.csv` |
| L9 | `./09-opensearch.sh` | opensearch logger → index → Grafana | `pav run -m pbs opensearch_verify` → `qstat -a` → `python3 ~/opensearch_results.py --name opensearch_verify` |
| L10 | `./10-mysql.sh` | mysql logger → MySQL table | `pav run demo_pbs.metrics` → `qstat -a` → `mysql pavilion -e "SELECT pav_id,name,result,sys_name,ROUND(duration,3) dur FROM results ORDER BY logged_at DESC LIMIT 5"` |
| saLog | `./12-salog.sh` | saLog CSV logger (run → PBS → CSV) | `pav run demo_pbs.salog` → `qstat -a` → `tail salog_output.txt` |

Then open **Grafana**: `http://<your-grafana-host>:3000`.

## Gotchas / fallbacks

- **L4 (PBS) timing:** run `pav run …` then *immediately* `qstat -a` to catch the job before it finishes.
- **L6 (series):** two sets (`smoke` + `perf`), `ordered: False` on purpose — ordered series need a background manager and can stall. Run it **on its own**, not immediately after another heavy run, and give it ~30s to reach COMPLETE.
- **L9:** the read-back auto-loads the password from `pavilion.yaml`, so no `OS_PASS` needed. The 08-output-csv demo is a safe fallback if OpenSearch is unhappy.
- **L10 (MySQL):** MariaDB must be running on pbs-server (`systemctl status mariadb`). The `mysql` CLI as the `pavilion` user auths via unix_socket (no password). The logger is **non-fatal** — if MySQL is down, other demos still pass (results just skip the MySQL row).
- **⚠️ Do NOT display `pavilion.yaml` on screen** — it contains a plaintext OpenSearch password. Use the deck's redacted version.
- Nothing is destructive; re-running demos just adds more runs (which makes `recent`/`test-summary` richer).

## Where things live

- Demo scripts: `~/pav_demo/` on **pbs-server** (source of truth: `demo/` in this repo).
- Test/mode/series configs: `configs/` in this repo (deployed into `~/pavilion2/config/{suites,modes,series}`). See `configs/README.md`.
- MySQL result logger: `plugins/` in this repo (deployed into `~/pavilion2/config/plugins/result_output/`). See `plugins/README.md`.
- Command plugins + other loggers: `~/pavilion2/config/plugins/{command,result_output}/` (source: the framework project `../pavilion2/`).
- The deck + its build script: `deck/pavilion-workshop.pptx`, `deck/build_deck.py`.
