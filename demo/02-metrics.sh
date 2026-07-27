#!/usr/bin/env bash
# L2 — Result parsing: regex parsers pull numbers out of test output into results (PBS job).
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_pbs.yaml"   # see the 'metrics' test + its result_parse block
say "pav run demo_pbs.metrics"
out=$(pav run demo_pbs.metrics); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show
pav wait "$sid" >/dev/null 2>&1
pause
say "pav results --full $sid   # parsed numbers land in results.json"
pav results --full "$sid" 2>&1 | grep -iE "throughput_mbs|latency_ms|errors|'result'|'name'"
