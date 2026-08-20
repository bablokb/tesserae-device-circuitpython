Installation on a Linux-PC/Laptop
=================================

Manual Installation
-------------------

The Tesserae-Client on a Linux system (laptop, desktop, Pi) needs
"Blinka", which provides the CircuitPython-API, PyGame for the UI and
a shim that uses PyGame to emulate a native (hardware) CircuitPython
display.

Run the following commands to install the environment:

    sudo apt-get -y install swig python3-dev
    python3 -m venv --system-site-packages venv.tesserae.cp-client
    . venv.tesserae.cp-client/bin/activate
    pip install blinka-displayio-pygamedisplay
    pip install adafruit-circuitpython-display-text

The first command *might* be necessary if pip needs to compile a
package from source.. If it does not cause problems due to
dependencies, the option `--system-site-packages` reduces the
necessary install time since it reuses already existing packages.


Configuration
-------------

Your `src/settings.py` should include the following lines to include
some boilerplate code supporting Blinka-Displayio-PyGameDisplay (see
`src/settings_template.py`):

    import board
    ...
    if (board.board_id == "GENERIC_LINUX_PC" or
        board.board_id.startswith("RASPBERRY_PI")):
      from settings_pygame import hw_config

Then, start the client with:

    export VENV=...path-to-venv
    TESSERAE_DISPLAY=native scripts/run-linux.sh

All emulated displays are defined in `src/pygame_display_info.py`. To
override settings (e.g. MAC-addresses), copy the file to `src/local`
and edit it there.

As an alternative to pre-defined displays, you can pass the display
configuration directly via `TESSERAE_DISPLAY`:

    TESSERAE_DISPLAY="name,width,height[,gamut[,[MAC]]]".

`gamut` defaults to `rgb16`. An empty MAC but a trailing comma will
select the hardware MAC. A missing MACs will autogenerate a stable MAC
based on the value of `TESSERAE_DISPLAY`.

Note: all software prereqs are also available for MacOS and Windows.
macOS is confirmed working — see [macOS Installation](./mac-install.md); it
reuses the Linux HAL and needs no platform-specific HAL file. Windows
is untested but should be similar. Contributions are welcome!
