Installation on a Raspberry Pi
==============================

**Important**: this document is not targeted at a Raspberry Pi with an e-ink
attached via display HAT (e.g. an Inky-Impression from Pimoroni). For these
devices, use the native client instead.

If you are running the Pi system as a *desktop* system, you should
follow the instructions in the document [PC/Laptop
Installation](./pc-install.md). For an appliance the recommended
installation is to follow the script-based installation described
here. Typical use cases are a Raspberry Pi together with an attached
HDMI/DSI monotor, e.g. a Pi-Touch-Display-2.

The [configuration section](./pc-install.md#configuration) of the
manual installation instructions is also relevant for Pi-appliances
and not repeated here.


Automatic Installation
----------------------

Use the automatic installation script to turns your system into a
dedicated dashboard system.

The script assumes a pre-installed PiOS-lite (tested with
Debian-Trixie). After cloning the repo, run:

    sudo scripts/pi-install.sh

The script first installs a number of system-packages needed for
direct rendering in console mode. Then it will create a Python virtual
environment just like the manual installation method does.

The script will also create a system-user `tesserae_client` with
HOME-directory `/usr/local/lib/tesserae_client`, create a venv in this
directory, and install a systemd-service. The configuration file
`settings.py` for the program is linked to
`/etc/tesserae-device-circuitpython/settings.py`. Configure everything
as needed there. Also, select the correct value of `TESSERAE_DISPLAY`
in `/etc/tesserae-device-circuitpython/env.sh`.


Uing Read-Only Mode
-------------------

PiOS supports a special "read-only" mode which can be useful for a
dashboard system. Since the Tesserae-client persists only the token
and a hash of the last requested dashboard, the read-only mode will
allow you to just turn the system off without shutdown.

For systems with a normal HDMI/DSI-display, there is no drawback. For
e-ink systems, there is one additional dashboard request plus update
at each power on.

It is important to activate the read-only mode *after* the client
registered with the server and stored the token. Use `raspi-config`,
section "Performance" to activate the read-only mode. This can be
undone again later, e.g. before an update of the firmware.
