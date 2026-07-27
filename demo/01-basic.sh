#!/usr/bin/env bash
# L1 — Basics: a PASS and an intentional FAIL, submitted as PBS jobs.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_pbs.yaml"   # the test definitions we're about to run
say "pav run demo_pbs.pass demo_pbs.fail"
out=$(pav run demo_pbs.pass demo_pbs.fail); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # proof it went through the scheduler
pav wait "$sid" >/dev/null 2>&1
pause
say "pav status $sid"; pav status "$sid"
pause
say "pav results $sid"; pav results "$sid"
