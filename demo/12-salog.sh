#!/usr/bin/env bash
# saLog — our NASA/NOAA CSV logger. Show it end-to-end: run in pav -> job in PBS -> CSV row.
source "$(dirname "$0")/_lib.sh"
cd /home/pavilion/pavilion2
say "pav --quiet run demo_pbs.pass demo_pbs.fail   # 1. run in Pavilion"
out=$(pav --quiet run demo_pbs.pass demo_pbs.fail); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # 2. the jobs, running in PBS
pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "tail -3 salog_output.txt        # 3. the CSV saLog wrote as nodes were released"
tail -3 salog_output.txt
