#!/usr/bin/env bash
# L9 — Custom OUTPUT plugin (mine): opensearch logger -> pavilion-results index -> Grafana.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run -m pbs opensearch_verify   # 4 PBS tests; each result ships to OpenSearch"
out=$(pav --quiet run -m pbs opensearch_verify); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # through the scheduler
pav --quiet wait "$sid" >/dev/null 2>&1
pause
# Export OS_PASS in your shell before the demo (never hard-code a password).
: "${OS_PASS:?Set OS_PASS in your environment first}"
say "python3 ~/opensearch_results.py --name opensearch_verify --limit 6   # read them back from the index"
python3 /home/pavilion/opensearch_results.py --name opensearch_verify --limit 6
echo; echo "Then open your Grafana dashboards."
