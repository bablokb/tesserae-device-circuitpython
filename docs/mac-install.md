Installation on macOS
======================

Like the Linux install, the Tesserae-Client on macOS runs on top of
"Blinka" (the CircuitPython-API for CPython), PyGame for the UI and a
shim that makes PyGame behave (almost) like a native CircuitPython
display.

No macOS-specific HAL file is needed. Blinka cannot auto-detect a Mac,
but forcing it to identify as a generic Linux-PC lets the client reuse
the existing `GENERIC_LINUX_PC` HAL unchanged (see step 3).

Tested on macOS (Apple Silicon) with Homebrew Python 3.14.


1. Install the environment
--------------------------

    python3 -m venv venv.tesserae.cp-client
    . venv.tesserae.cp-client/bin/activate
    pip install blinka-displayio-pygamedisplay
    pip install adafruit-circuitpython-display-text


2. Pin setuptools (Python 3.12+)
--------------------------------

Recent Python (e.g. the Homebrew 3.14 build) no longer ships
`pkg_resources`, but Blinka and PyGame still import it. Install a
setuptools version that still provides it:

    pip install "setuptools<81"

Without this, `import board` fails with `ModuleNotFoundError: No module
named 'pkg_resources'`.


3. Force the Blinka board identity
----------------------------------

Note: this is for documentation only. The generic run-script
(`scripts/run-client.sh`, see below) will take care of exporting all
necessary variables.

`adafruit-platformdetect` does not recognise the "Darwin" platform and
raises `NotImplementedError` from `import board` before any HAL is even
selected. Tell Blinka to present itself as a generic Linux-PC:

    export BLINKA_FORCEBOARD=GENERIC_LINUX_PC
    export BLINKA_FORCECHIP=GENERIC_X86

With this, `board.board_id` returns `GENERIC_LINUX_PC`, so the client
loads the stock `external/base-app/base_app/hal/GENERIC_LINUX_PC.py`
HAL. (A harmless `GENERIC_X86 is not fully supported` warning is
printed.)


4. Configuration and Running
----------------------------

To start the client, execute `scripts/run-client.sh`. Read the
relevant section in the [PC installation guide](./pc-install.md) for
available options.

Note: launch the script from a normal Terminal (Terminal.app / iTerm),
i.e. a real GUI login session. A pygame window created from a
background / non-interactive process may register in the app-switcher
but never actually appear on screen.
