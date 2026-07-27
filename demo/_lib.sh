# Sourced by each demo script. Pretty-prints the command, then you see real pav output.
# (No --quiet needed: the config-label warning is fixed at the source — the builtins
#  config area now has a label via ~/pavilion2/builtins/config.yaml.)
say(){ printf '\n\033[1;36m$ %s\033[0m\n' "$*"; }
pause(){ [ -n "$NOPAUSE" ] || read -rp $'\n\033[2m(enter to continue)\033[0m ' _; }
# Show that the run actually went through the scheduler.
qstat_show(){ say "qstat -a"; qstat -a; }
# Where the Pavilion configs live on the cluster.
CFG="$HOME/pavilion2/config"
# Cat the YAML that defines the test we're about to run, so the audience sees it first.
show_yaml(){ say "cat $1"; cat "$1"; pause; }
