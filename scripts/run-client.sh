#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# run-client.sh: launch the Tesserae CircuitPython client.
#
# Usage:  ./scripts/run-client.sh
#         ./scripts/run-client.sh ii4
#
# The first example emulates the "native" display, the second example
# emulates the "ii4"-display (4"-Inky-Impression).
#
# For a complete list of pre-defined displays, run
#     ./scripts/run-client.sh -v -L
#
# Ad-hoc definitions are also possible:
#   ./scripts/run-client.sh "mydisplay,400,300,rgb16,02:00:00:AB:CD:EF"
#
# Notes:
#   - Format for display spec  is: "name,width,height[,gamut[,[MAC]]]".
#   - An empty MAC but a trailing comma will select the hardware MAC.
#   - A missing MACs will autogenerate a stable MAC based on
#     TESSERAE_DISPLAY.
#   - No spaces are allowed in spec
#
# ----------------------------------------------------------------------------
#set -euo pipefail

pgmDir=$(dirname "$0")
pgmName=$(basename "$0")

# write message to stderr   --------------------------------------------------

msg() {
  local type="$1"
  shift
  if [ "$type" = "info" -a $quiet -eq 0 -o \
       "$type" = "debug" -a $debug -eq 1 -o \
       "$type" = "warning" -o "$type" = "error" ]; then
    echo -e "[$type] $@" >&2
  fi
}

# set defaults   --------------------------------------------------------------

setDefaults() {
  quiet=0; simulate=0; debug=0; verbose=0
  action="run"

  # default for client source-directory
  src="$(dirname "$0")/../src"

  # default for venv
  if [ -n "$VENV" ]; then
    venv=$(realpath -q "$VENV")
    return
  fi

  # check a number of standard locations for venv
  for d in \
    "./venv.tesserae" \
    "./venv.tesserae.cp-client" \
    "$(dirname "$0")/../venv.tesserae.cp-client" \
    "$HOME/venv.tesserae" \
    "$HOME/venv.tesserae.cp-client"; do
    d=$(realpath -q "$d")
    if [ -d "$d" ]; then
      venv="$d"
      break
    fi
  done
}

# usage message   -------------------------------------------------------------

usage() {
  echo -e "\n`basename $0`: run Tesserae-Client\n\
  \nusage: `basename $0` [options] display\n\
  possible options:\n\
    -V venv path to virtual environment\n\
    -S src  path to client soure-directory\n\
    -L      list predefined displays\n\

    -h     show this help\n\
    -q     run quiet\n\
    -v     verbose output\n\
    -s     only simulate\n\
    -d     print debug output\n\
" >&2
  exit 3
}

# parse arguments and set variables -------------------------------------------

parseArguments() {
  while getopts ":V:S:Lhqvsd" opt; do
    case $opt in
      V) venv=$(realpath -q "$OPTARG");;
      S) src=$(realpath -q "$OPTARG");;
      L) action="list_displays";;
    h) usage;;
    q) quiet=1;;
    v) verbose=1;;
    s) simulate=1;;
    d) debug=1;;
    ?) echo "error: illegal option: $OPTARG" >&2
         usage;;
    esac
  done
  shift $((OPTIND-1))
  display="$1"
}

# execute a command   ----------------------------------------------------------

do_cmd() {
  if [ $simulate -eq 0 ]; then
    msg 'debug' "executing: $@"
    eval "$@"
    return $?
  else
    msg 'info' "simulating: $@"
    return 0
  fi
  return 0
}

# check arguments   ------------------------------------------------------------

checkArguments() {
  if [ ! -d "$src" ]; then
    msg "error" "client source-directory does not exist at: $src"
    usage
  fi
  if [ "$action" = "run" ]; then
    if [ -z "$venv" ]; then
      msg "error" "no venv defined"
      usage
    fi
    if [ ! -d "$venv" ]; then
      msg "error" "virtual environment does not exist at: $venv"
      usage
    fi
    if [ -z "$display" ]; then
      msg "error" "missing display argument"
      usage
    fi
  fi
}

# main program   ---------------------------------------------------------------

setDefaults
parseArguments "$@"
checkArguments

msg "info" "using venv: $venv"
msg "info" "using src: $src"
msg "info" "using display: $display"

if [ "$action" = "list_displays" ]; then
  echo -e "Available displays:\n"
  do_cmd python3 "$src/pygame_display_info.py" "$verbose"
  echo -e
  exit 0
else
  if [[ "$OSTYPE" == darwin* ]]; then
    export BLINKA_FORCEBOARD="${BLINKA_FORCEBOARD:-GENERIC_LINUX_PC}"
    export BLINKA_FORCECHIP="${BLINKA_FORCECHIP:-GENERIC_X86}"
  fi 
  export TESSERAE_DISPLAY="$display"
  cd "$src"
  do_cmd "$venv/bin/python3" ./main.py
fi
