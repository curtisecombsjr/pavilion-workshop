#!/usr/bin/env bash
# L5 — Modes: a reusable overlay that changes a test at run time (-m).
source "$(dirname "$0")/_lib.sh"
say "pav show modes"; pav --quiet show modes
say "pav --quiet run demo_modes.mode_demo            # plain -> label=default"
o1=$(pav --quiet run demo_modes.mode_demo); s1=$(echo "$o1" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$s1" >/dev/null 2>&1
pav --quiet results --full "$s1" 2>&1 | grep -oE "'label': '[^']*'" | head -1
pause
say "pav --quiet run -m prod demo_modes.mode_demo    # with mode -> label=production"
o2=$(pav --quiet run -m prod demo_modes.mode_demo); s2=$(echo "$o2" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$s2" >/dev/null 2>&1
pav --quiet results --full "$s2" 2>&1 | grep -oE "'label': '[^']*'" | head -1
