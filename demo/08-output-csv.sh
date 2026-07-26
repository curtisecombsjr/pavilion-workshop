#!/usr/bin/env bash
# L8 — csv_file logger. Run a real PBS job (qstat proves dispatch), then show the CSV row.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_echo.demo_pass_pbs      # a real PBS job"
out=$(pav --quiet run demo_echo.demo_pass_pbs); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
say "qstat -a                             # it went through the scheduler"; qstat -a
pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "tail -4 /home/pavilion/pav_logs/results.csv   # one row per test"
tail -4 /home/pavilion/pav_logs/results.csv | cut -c1-100
