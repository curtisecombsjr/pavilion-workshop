#!/usr/bin/env bash
# L7 — Custom COMMAND plugins (mine): new pav subcommands. (No test YAML — these are Python plugins.)
source "$(dirname "$0")/_lib.sh"
say "pav hello --name Team";        pav hello --name Team
pause
say "pav recent -n 6";             pav recent -n 6
pause
say "pav test-summary";            pav test-summary
pause
say "pav disk-usage";              pav disk-usage
