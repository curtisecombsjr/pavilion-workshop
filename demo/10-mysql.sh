#!/usr/bin/env bash
# L10 — Custom OUTPUT plugin (mine): mysql logger writes a row per result into MySQL.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_echo.demo_metrics   # every logger fires, incl. mysql"
out=$(pav --quiet run demo_echo.demo_metrics); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "mysql pavilion -e 'SELECT pav_id,name,result,dur FROM results ORDER BY logged_at DESC LIMIT 5'"
mysql pavilion -e "SELECT pav_id, name, result, ROUND(duration,3) AS dur FROM results ORDER BY logged_at DESC LIMIT 5"
