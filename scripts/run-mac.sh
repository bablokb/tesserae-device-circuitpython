#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# run-mac.sh: launch the Tesserae CircuitPython client on macOS.
#
# Blinka cannot auto-detect macOS, so we force the generic Linux-PC board
# identity; the existing GENERIC_LINUX_PC HAL is then reused unchanged.
# See mac-install.md for the one-time setup (venv + "setuptools<81").
#
# Usage:  ./scripts/run-mac.sh            # emulate the "native" display
#         TESSERAE_DISPLAY=ii4 ./run-mac.sh
# ----------------------------------------------------------------------------
set -euo pipefail

git_root="$(dirname "$0")/.."
venv="$git_root/venv.tesserae.cp-client"

if [ ! -x "$venv/bin/python3" ]; then
  echo "error: venv not found at $venv" >&2
  echo "run the setup in mac-install.md first." >&2
  exit 1
fi

export BLINKA_FORCEBOARD="${BLINKA_FORCEBOARD:-GENERIC_LINUX_PC}"
export BLINKA_FORCECHIP="${BLINKA_FORCECHIP:-GENERIC_X86}"
export TESSERAE_DISPLAY="${TESSERAE_DISPLAY:-native}"

cd "$git_root/src"
exec "$venv/bin/python3" ./main.py
