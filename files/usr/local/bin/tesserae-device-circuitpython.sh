#!/bin/bash
# ----------------------------------------------------------------------------
# Wrapper for Tesserae Device Client CircuitPython.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

TESSERAE_ROOT="/usr/local/lib/tesserae_client/"
VENV="$TESSERAE_ROOT/venv.tesserae"
SRC="$TESSERAE_ROOT/tesserae-device-circuitpython/src"

. /etc/tesserae-device-circuitpython/env.sh

cd "$SRC"
exec "$VENV/bin/python3" ./main.py
