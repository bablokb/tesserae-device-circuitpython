Installation on a Linux-PC/Laptop
=================================

Manual Installation
-------------------

The Tesserae-Client on a Linux system (laptop, desktop, Pi) needs
"Blinka", which provides the CircuitPython-API, PyGame for the UI and
a shim that uses PyGame to emulate a native (hardware) CircuitPython
display.

Run the following commands to install the environment:

    #sudo apt-get -y install swig python3-dev
    python3 -m venv --system-site-packages venv.tesserae.cp-client
    . venv.tesserae.cp-client/bin/activate
    pip install blinka-displayio-pygamedisplay
    pip install adafruit-circuitpython-display-text

The first command *might* be necessary if pip needs to compile a
package from source. Adding `--system-site-packages` while creating
the venv was needed on a Pi5, but not on a Pi3. If it does not
cause problems due to dependencies, this switch also reduces the
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

    (cd src; TESSERAE_DISPLAY=native python3 ./main.py)

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
macOS is confirmed working — see [macOS Install](./mac-install.md); it
reuses the Linux HAL and needs no platform-specific HAL file. Windows
is untested but should be similar. Contributions are welcome!


Automatic Installation
----------------------

**Implemented soon**

Use the automatic installation script to turn your system into a
dedicated dashboard system. Typically used on a Pi-class device with
attached HDMI/DSI monitor. A Pi with a display HAT (e.g. an
Inky-Impression from Pimoroni) does not use Blinka. In this case, use
a native client instead.

The script assumes that the OS is Debian based. After cloning the
repo (or just downloading the script), run:

    sudo scripts/pi-install.sh

This will create a system-user `tesserae` with HOME-directory
`/usr/local/lib/tesserae`, create a venv in this directory, clone the
repo and install a systemd-service. The configuration file
`settings.py` for the service is in
`/usr/local/lib/tesserae/tesserae-device-circuitpython/src`.

A dedicated Pi-based dashboard might or might not need a graphical
desktop environment. The Pi-Touchdisplay-2 works fine with the lite
version of PiOS, while a HDMI attached Waveshare 7"-display needed a
graphical desktop. This depends on SDL, the rendering layer used by
PyGame.
