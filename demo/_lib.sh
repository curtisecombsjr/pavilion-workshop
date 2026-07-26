# Sourced by each demo script. Pretty-prints the command, then you see real pav output.
say(){ printf '\n\033[1;36m$ %s\033[0m\n' "$*"; }
pause(){ [ -n "$NOPAUSE" ] || read -rp $'\n\033[2m(enter to continue)\033[0m ' _; }
