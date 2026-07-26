#!/usr/bin/env bash
# L1 — Basics: a PASS and an intentional FAIL via the raw (local) scheduler.
source "$(dirname "$0")/_lib.sh"
say "pav --quiet run demo_echo.demo_pass_raw demo_echo.demo_fail_raw"
out=$(pav --quiet run demo_echo.demo_pass_raw demo_echo.demo_fail_raw); echo "$out"
sid=$(echo "$out" | grep -oE 's[0-9]+' | head -1); pav --quiet wait "$sid" >/dev/null 2>&1
pause
say "pav --quiet status $sid"; pav --quiet status "$sid"
pause
say "pav --quiet results $sid"; pav --quiet results "$sid"
