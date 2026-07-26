#!/usr/bin/env bash
# L2 — Result parsing: regex parsers pull numbers out of test output into results (PBS job).
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_pbs.metrics"
out=$(pav --quiet run demo_pbs.metrics); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show
pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet results --full $sid   # parsed numbers land in results.json"
pav --quiet results --full "$sid" 2>&1 | grep -iE "throughput_mbs|latency_ms|errors|'result'|'name'"
