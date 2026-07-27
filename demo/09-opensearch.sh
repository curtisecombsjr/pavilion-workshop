#!/usr/bin/env bash
# L9 — Custom OUTPUT plugin (mine): opensearch logger -> pavilion-results index -> Grafana.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/opensearch_verify.yaml"   # the tests we ship to OpenSearch
say "pav run -m pbs opensearch_verify   # 4 PBS tests; each result ships to OpenSearch"
out=$(pav run -m pbs opensearch_verify); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # through the scheduler
pav wait "$sid" >/dev/null 2>&1
pause
# No OS_PASS needed: opensearch_results.py auto-loads the password from pavilion.yaml
# (env OS_PASS still overrides if you want). Nothing is hard-coded or displayed.
say "python3 ~/opensearch_results.py --name opensearch_verify --limit 6   # read them back from the index"
python3 /home/pavilion/opensearch_results.py --name opensearch_verify --limit 6
echo; echo "Then open your Grafana dashboards."
