#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# run-linux.sh: launch the Tesserae CircuitPython client on Linux.
#
# Usage:  ./scripts/run-linux.sh
#         TESSERAE_DISPLAY=ii4 ./scripts/run-linux.sh
#
# The venv must be within the repository root or exported as VENV.
#
# The first example emulates the "native" display, the second example
# emulates the "ii4"-display (4"-Inky-Impression).
#
# For a complete list of pre-defined displays, see src/pygame_display_info.py.
#
# Ad-hoc definitions are also possible:
#   TESSERAE_DISPLAY="mydisplay,400,300,rgb16,02:00:00:AB:CD:EF" \
#                                                   ./scripts/run-linux.sh
# Notes:
#   - Format for TESSERAE_DISPLAY is: "name,width,height[,gamut[,[MAC]]]".
#   - An empty MAC but a trailing comma will select the hardware MAC.
#   - A missing MACs will autogenerate a stable MAC based on
#     TESSERAE_DISPLAY.
#   - No spaces are allowed in TESSERAE_DISPLAY
#
# ----------------------------------------------------------------------------
set -euo pipefail

git_root="$(dirname "$0")/.."
venv="$(realpath ${VENV:-$git_root/venv.tesserae.cp-client})"

if [ ! -x "$venv/bin/python3" ]; then
  echo "error: venv not found at $venv" >&2
  echo "run the setup in pc-install.md first." >&2
  exit 1
fi

export TESSERAE_DISPLAY="${TESSERAE_DISPLAY:-native}"

cd "$git_root/src"
exec "$venv/bin/python3" ./main.py
