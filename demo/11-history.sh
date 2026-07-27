#!/usr/bin/env bash
# Record-keeping — search the whole run history with -F filters. (No single test YAML — searches all runs.)
source "$(dirname "$0")/_lib.sh"
say "pav status all -F failed                    # every failed run, all the way back"
pav status all -F "failed" 2>&1 | head -16
pause
say "pav status all -F 'name=demo_pbs.metrics'   # one test, every run"
pav status all -F "name=demo_pbs.metrics" 2>&1 | head -12
pause
say "pav status all -F 'name=demo_pbs.fail and failed'   # combine filters"
pav status all -F "name=demo_pbs.fail and failed" 2>&1 | head -8
