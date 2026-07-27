#!/usr/bin/env bash
# saLog — our NASA/NOAA CSV logger, driven by the sa_log result plugin.
# demo_pbs.salog writes a per-node .log (per_file: name), so the logger fires on release.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_pbs.yaml"   # see the 'salog' test: per_file: name feeds the logger
cd /home/pavilion/pavilion2            # saLog appends salog_output.txt in its own dir
say "pav run demo_pbs.salog   # 1. run in Pavilion"
out=$(pav run demo_pbs.salog); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # 2. the job, running in PBS
pav wait "$sid" >/dev/null 2>&1
pause
say "tail -3 salog_output.txt   # 3. the CSV the sa_log plugin wrote on node release"
tail -3 salog_output.txt
