#!/usr/bin/env bash
# L5 — Modes: a reusable overlay that flips the test FAIL -> PASS by overriding a value.
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_modes.yaml"   # the test: throughput 1200, must be > 1300
show_yaml "$CFG/modes/prod.yaml"          # the mode overlay: throughput -> 1400
say "pav run demo_modes.mode_demo            # base throughput=1200 -> FAIL (not > 1300)"
o1=$(pav run demo_modes.mode_demo); s1=$(echo "$o1" | grep -oE 's[0-9]+' | head -1)
qstat_show   # runs through PBS
pav wait "$s1" >/dev/null 2>&1
pav results --full "$s1" 2>&1 | grep -iE "throughput_mbs|'result'"
pause
say "pav run -m prod demo_modes.mode_demo    # prod overrides throughput=1400 -> PASS"
o2=$(pav run -m prod demo_modes.mode_demo); s2=$(echo "$o2" | grep -oE 's[0-9]+' | head -1)
pav wait "$s2" >/dev/null 2>&1
pav results --full "$s2" 2>&1 | grep -iE "throughput_mbs|'result'"
