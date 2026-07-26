#!/usr/bin/env bash
# L3 — Permutations: one config x variable lists => many test instances.
source "$(dirname "$0")/_lib.sh"
say "cat config/suites/demo_perms.yaml   # permute_on: [size, mode]  (3 x 2)"
say "pav --quiet run demo_perms.matrix   # creates 6 tests from ONE definition"
out=$(pav --quiet run demo_perms.matrix); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet status $sid"; pav --quiet status "$sid"
