#!/usr/bin/env bash
# L5 — Modes: a reusable overlay that changes a test at run time (-m).
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_modes.yaml"   # the test: env_label defaults to 'default'
show_yaml "$CFG/modes/prod.yaml"          # the mode overlay: env_label -> 'production'
say "pav show modes"; pav show modes
say "pav run demo_modes.mode_demo            # plain -> label=default"
o1=$(pav run demo_modes.mode_demo); s1=$(echo "$o1" | grep -oE 's[0-9]+' | head -1); pav wait "$s1" >/dev/null 2>&1
pav results --full "$s1" 2>&1 | grep -oE "'label': '[^']*'" | head -1
pause
say "pav run -m prod demo_modes.mode_demo    # with mode -> label=production"
o2=$(pav run -m prod demo_modes.mode_demo); s2=$(echo "$o2" | grep -oE 's[0-9]+' | head -1)
qstat_show   # the mode still runs through PBS
pav wait "$s2" >/dev/null 2>&1
pav results --full "$s2" 2>&1 | grep -oE "'label': '[^']*'" | head -1
