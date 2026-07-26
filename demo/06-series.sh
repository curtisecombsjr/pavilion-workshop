#!/usr/bin/env bash
# L6 — Series: run a whole group of test sets with one command (each set -> a PBS job).
source "$(dirname "$0")/_lib.sh"
say "cat config/series/demo_series.yaml   # smoke + perf (2 PBS test sets)"
say "pav series run demo_series"
out=$(pav --quiet series run demo_series 2>&1); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # one PBS job per test set
say "waiting for the series..."; sleep 32
pause
say "pav --quiet series status $sid"; pav --quiet series status "$sid"
