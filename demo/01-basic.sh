#!/usr/bin/env bash
# L1 — Basics: a PASS and an intentional FAIL, submitted as PBS jobs.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_pbs.pass demo_pbs.fail"
out=$(pav --quiet run demo_pbs.pass demo_pbs.fail); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # proof it went through the scheduler
pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet status $sid"; pav --quiet status "$sid"
pause
say "pav --quiet results $sid"; pav --quiet results "$sid"
