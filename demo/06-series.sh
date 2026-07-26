#!/usr/bin/env bash
# L6 — Series: run a whole group of test sets with one command.
source "$(dirname "$0")/_lib.sh"
say "cat config/series/demo_series.yaml   # smoke + metrics + matrix (8 tests)"
say "pav series run demo_series"
out=$(pav --quiet series run demo_series 2>&1); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
say "waiting for the series..."; sleep 15
pause
say "pav --quiet series list   # the series summary row"; pav --quiet series list 2>&1 | sed -n '1,3p'; pav --quiet series list 2>&1 | grep " $sid "
