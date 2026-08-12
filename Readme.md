Generic Tesserae Device Firmware
================================

**WORK IN PROGRESS, see [Status](#status "Status") below**


Overview
--------

This repository implements a
[Tesserae](https://github.com/dmellok/tesserae) client using
CircuitPython. Tesserae is a dashboard server, the role of the client
is to poll for an updated dashboard and display it on a display. For
alternative (native) clients and to learn about the full power of
Tesserae, visit the Tesserae repository or the [Tesserae
dokumentation](https://docs.tesserae.ink/).

CircuitPython runs on as of today 655 boards. It also runs on a normal
laptop/PC using Blinka. So the rationale of this project is to provide
a generic client that runs on all boards that support CircuitPython and
are powerful enough to drive a display.

This repository uses at it's core the [CircuitPython Base
App](https://github.com/bablokb/circuitpython-base-app) that provides
the logic to pull data, update a display and go to sleep (or shutdown)
afterwards.

While CircuitPython already provides a stable API across architectures
and boards, two additional levels of abstraction are necessary. A
*hardware abstraction layer* (HAL) and a *configuration layer*. The
HAL will deal with board-specific peripherals (e.g. buttons, low-power
electronics), while the configuration layer allows a given board to run
with different peripherals (e.g. displays or buttons).

The core take away is: this client will not automagically run on any
device. But to make it run, it is only necessary to create a suitable
configuration and maybe to create the necessary HAL.


Status
------

This list is not a priority list.

  - [ ] Improve documentation
  - [ ] Support memory constrained systems by caching files on SD
  - [ ] Add example configurations for more hardware devices
  - [ ] Support buttons
  - [ ] Automated setup of PiOS based clients (using cloud-init)
  - [ ] Support touch displays
  - [X] Client side scheduled wakeup and polling
  - [X] Support "on/off" or "on/deep-sleep" workflows for devices
        running on batteries
  - [X] Honor ETAG / 304 on e-ink displays
  - [X] Memory optimized download of dashboards 
  - [X] Application configuration
  - [X] Emulation of arbitrary displays using PyGame-Displayio
  - [X] Basic workflow for "always-on" devices is functional


Hardware Requirements
---------------------

CircuitPython itself uses a fair amount of RAM. This limits the
available memory for the operation of a client. The client mainly
needs memory for the network stack and the bitmap that is drawn on the
display.

ESP32S2/ESP32S3 base systems with PSRAM are usually a better choice
than other systems. E.g. the Inky-Frame 5.7 has a display with 600x448
pixels and is driven by an embedded Pico-W. This combination cannot
download the dashboard and update the display in one go. The second
generation Inky-Frame 7.3 with a Pico2-W in contrast does work.

Another aspect is support for deep-sleep. While the Inky-Frames
support very low power states due to special hardware, other
RP2xxx-devices use much more energy compared to ESP32xx
systems. Mainline CircuitPython doesn't even have support for
RP2350 deep-sleep at all.


Tested Devices
--------------

Successfully tested:

  - **Pico-W with SharpMemory-Display (420x200)**
  - **Inky-Impression 7.3** (Spectra6) with Pico2-W (with adapter)
  - **Adafruit MagTag**
  - **Blinka with PyGame-Displayio** on Linux, Pi3, Pi5
  - **Blinka with PyGame-Displayio** on MacOS

Failed devices:

  - **Pimoroni Inky-Frame-5.7** (embedded Pico-W): MemoryError.
    This device might work once caching on SD is implemented.


Installation
------------

This repository uses submodules, so you either need to clone with

    git clone --recurse-submodules https://github.com/bablokb/tesserae-device-circuitpython

or update the submodules after a normal clone:

    git clone https://github.com/bablokb/tesserae-device-circuitpython
    git submodule update --init --recursive

See [PC/Laptop Install](./docs/pc-install.md) for how to install this
client on a Linux-PC.

See [macOS Install](./docs/mac-install.md) for how to install this
client on a Mac. No macOS-specific HAL is needed: forcing Blinka to
identify as a generic Linux-PC lets the existing `GENERIC_LINUX_PC`
HAL be reused unchanged.

See [CircuitPython Device Install](./docs/mcu-install.md) for how to
install this client on a MCU.


Configuration
-------------

The central configuration file is `src/settings.py` which is not
tracked by the repository. Copy the blueprint `src/settings_template.py`
to `src/settings.py` and edit where appropriate.

The file creates three `Settings`-objects:

  - `secrets`: WLAN credentials (only needed for real hardware)
  - `app_config`: application configuration
  - `hw_config`: hardware configuration

For all the details about `secrets` and `hw_config`, see the [base app
documentation](https://github.com/bablokb/circuitpython-base-app/config-reference-md).

Some simpler hardware configuration examples and HOWTOs are in [hw_config
examples](./docs/hw_config.md).

The reference for application specific configuration is
[here}(./docs/app_config.md).


Contributing
------------

For new HAL files for specific hardware boards create a PR in the
Base App repo.

To add a configuration layer example, create a PR here.
