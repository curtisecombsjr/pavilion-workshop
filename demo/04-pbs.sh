#!/usr/bin/env bash
# L4 — PBS scheduler: submit, see it RUNNING in Pavilion and PBS, then results.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_pbs.yaml"   # note scheduler: pbs + the schedule block
say "pav run demo_pbs.pass"
out=$(pav run demo_pbs.pass); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
pause
say "pav status $sid   # Pavilion sees it running"; pav status "$sid"
say "qstat -a                  # PBS sees the same job"; qstat -a
say "waiting for the PBS job to finish..."; pav wait "$sid" >/dev/null 2>&1
pause
say "pav results $sid"; pav results "$sid"
