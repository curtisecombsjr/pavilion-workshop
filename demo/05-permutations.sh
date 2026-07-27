#!/usr/bin/env bash
# L3 — Permutations: one config x variable lists => many test instances.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_perms.yaml"   # permute_on: [size, mode] (3 x 2), one job per instance
say "pav run demo_perms.matrix   # creates 6 tests from ONE definition"
out=$(pav run demo_perms.matrix); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # all six ride PBS jobs
pav wait "$sid" >/dev/null 2>&1
pause
say "pav status $sid"; pav status "$sid"
