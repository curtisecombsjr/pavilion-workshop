#!/usr/bin/env bash
# Inheritance — 'base' holds shared config; children inherit_from it and override only their delta.
#   small = inherits everything | large = overrides the variable | debug = overrides the build
source "$(dirname "$0")/_lib.sh"
show_yaml "$CFG/suites/demo_inherit.yaml"   # base + small/large/debug (inherits_from)
say "pav run demo_inherit.small demo_inherit.large demo_inherit.debug"
out=$(pav run demo_inherit.small demo_inherit.large demo_inherit.debug); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1)
qstat_show   # each is its own PBS job (small & large reuse base's build)
pav wait "$sid" >/dev/null 2>&1
pause
say "pav results --full $sid   # inherited vs overridden, per child"
pav results --full "$sid" 2>&1 | grep -E "'name'|'flags'|'threads'"
