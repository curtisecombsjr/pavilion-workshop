#!/usr/bin/env bash
# L2 — Result parsing: regex parsers pull numbers out of test output into results.
source "$(dirname "$0")/_lib.sh"
say "cat config/suites/demo_echo.yaml   # (show the demo_metrics result_parse block)"
say "pav --quiet run demo_echo.demo_metrics"
out=$(pav --quiet run demo_echo.demo_metrics); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet results --full $sid   # parsed numbers land in results.json"
pav --quiet results --full "$sid" 2>&1 | grep -iE "throughput_mbs|latency_ms|errors|'result'|'name'"
