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

The automatic installation script to turns your system into a
dedicated dashboard system.

The script assumes a pre-installed PiOS-lite (tested with
Debian-Trixie). After cloning the repo, run:

    scripts/pi-install.sh

The script first installs a number of system-packages needed for
direct rendering in console mode. Then it will create a Python virtual
environment just like the manual installation method does.

** to be implemented soon:**

The script will also create a system-user `tesserae` with
HOME-directory `/usr/local/lib/tesserae`, create a venv in this
directory, and install a systemd-service. The configuration file
`settings.py` for the service is in
`/usr/local/lib/tesserae/tesserae-device-circuitpython/src`, but
usually it is only necessary to change the value of `TESSERAE_DISPLAY`
in `/etc/tesserae-device-circuitpython.conf`.
