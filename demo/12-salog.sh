#!/usr/bin/env bash
# saLog — our NASA/NOAA CSV logger (emulation script on pbs-server). Flags: -n -c -u -a.
source "$(dirname "$0")/_lib.sh"
cd /home/pavilion/pavilion2
say "cat saLog        # the emulator — flags: -n node  -c content  -u user  -a action"
cat saLog
pause
say "./saLog -n x1003c7s7b0n3 -c 'pav_test result=PASS' -u pavilion -a released"
./saLog -n x1003c7s7b0n3 -c 'pav_test result=PASS' -u pavilion -a released
say "tail -3 salog_output.txt        # appends a CSV row"
tail -3 salog_output.txt
