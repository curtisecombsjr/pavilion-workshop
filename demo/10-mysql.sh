#!/usr/bin/env bash
# L10 — Custom OUTPUT plugin (mine): mysql logger writes a row per result into MySQL (PBS job).
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_pbs.metrics   # every logger fires, incl. mysql"
out=$(pav --quiet run demo_pbs.metrics); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # a real PBS job
pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "mysql pavilion -e 'SELECT pav_id,name,result,sys_name,dur FROM results ORDER BY logged_at DESC LIMIT 5'"
mysql pavilion -e "SELECT pav_id, name, result, sys_name, ROUND(duration,3) AS dur FROM results ORDER BY logged_at DESC LIMIT 5"
