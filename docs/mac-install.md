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

`adafruit-platformdetect` does not recognise the "Darwin" platform and
raises `NotImplementedError` from `import board` before any HAL is even
selected. Tell Blinka to present itself as a generic Linux-PC:

    export BLINKA_FORCEBOARD=GENERIC_LINUX_PC
    export BLINKA_FORCECHIP=GENERIC_X86

With this, `board.board_id` returns `GENERIC_LINUX_PC`, so the client
loads the stock `external/base-app/base_app/hal/GENERIC_LINUX_PC.py`
HAL. (A harmless `GENERIC_X86 is not fully supported` warning is
printed.)


4. Configure
------------

Copy `src/settings_template.y` to `src/settings.py` and edit where
appropriate (at minimum `app_config.url`).

Note: the Linux HAL reads the MAC address from `/sys/class/net/`, which
does not exist on macOS, so it reports `None`. If your server keys
devices by MAC, set a fixed value in `settings.py` so registration is
stable across runs:

    app_config.mac = "02:00:00:ca:fe:01"


5. Run
------

Use the helper script, which sets the env vars above for you:

    ./run-mac.sh                    # emulate the "native" display
    TESSERAE_DISPLAY=ii4 ./run-mac.sh

For a list of valid displays to emulate, see `src/settings_pygame.py`.

Note: launch it from a normal Terminal (Terminal.app / iTerm), i.e. a
real GUI login session. A pygame window created from a background /
non-interactive process may register in the app-switcher but never
actually appear on screen.
