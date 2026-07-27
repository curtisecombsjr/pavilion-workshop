#!/usr/bin/env bash
# Result evaluation — result_evaluate turns a parsed number into PASS/FAIL (rule: score > 100).
# Both tests exit 0; the evaluation, not the exit code, decides.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_eval.yaml"   # parse 'score', then evaluate: result = score > 100
say "pav run demo_eval.high demo_eval.low   # both exit 0 — the evaluation decides"
out=$(pav run demo_eval.high demo_eval.low); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show
pav wait "$sid" >/dev/null 2>&1
pause
say "pav results --full $sid   # result comes from 'score > 100', not the exit code"
pav results --full "$sid" 2>&1 | grep -E "'name'|'score'|'result'"
