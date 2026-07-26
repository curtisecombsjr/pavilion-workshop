#!/usr/bin/env bash
# L4 — PBS scheduler: submit, see it RUNNING in Pavilion and PBS, then results.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_pbs.pass"
out=$(pav --quiet run demo_pbs.pass); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
pause
say "pav --quiet status $sid   # Pavilion sees it running"; pav --quiet status "$sid"
say "qstat -a                  # PBS sees the same job"; qstat -a
say "waiting for the PBS job to finish..."; pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet results $sid"; pav --quiet results "$sid"
