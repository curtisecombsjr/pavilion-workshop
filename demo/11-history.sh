#!/usr/bin/env bash
# Record-keeping — search the whole run history with -F filters.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet status all -F failed                    # every failed run, all the way back"
pav --quiet status all -F "failed" 2>&1 | head -16
pause
say "pav --quiet status all -F 'name=demo_pbs.metrics'   # one test, every run"
pav --quiet status all -F "name=demo_pbs.metrics" 2>&1 | head -12
pause
say "pav --quiet status all -F 'name=demo_pbs.fail and failed'   # combine filters"
pav --quiet status all -F "name=demo_pbs.fail and failed" 2>&1 | head -8
