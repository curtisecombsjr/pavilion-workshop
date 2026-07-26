#!/usr/bin/env bash
# L7 — Custom COMMAND plugins (mine): new pav subcommands.
source "$(dirname "$0")/_lib.sh"
say "pav hello --name Team";        pav --quiet hello --name Team
pause
say "pav recent -n 6";             pav --quiet recent -n 6
pause
say "pav test-summary";            pav --quiet test-summary
pause
say "pav disk-usage";              pav --quiet disk-usage
