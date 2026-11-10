CEC Support
===========

CEC support is available for Pi appliances running with a TV set. The remote
control of the TV generates key events for the Tesserae-client.


Prerequisites
-------------

As a prerequisite you have to compile and install the Python bindings
for libcec provided by Pulse-Eight. **Don't install the pip packages `cec`
or `pyCEC` or the Debian-package `python3-pycec`.**

To compile and install, read the instructions from the [Pulse-Eight
documentation](https://github.com/Pulse-Eight/libcec/blob/master/docs/README.raspberrypi.md).

At the time of this writing, the necessary commands on top of what
`scripts/pi-install.sh` already installed were:

    sudo apt-get update
    sudo apt-get -y install cmake
    cd
    git clone https://github.com/Pulse-Eight/libcec.git
    mkdir libcec/build
    cd libcec/build
    cmake  -DHAVE_LINUX_API=1 -DHAVE_RPI_API=0 ..
    make -j4
    sudo make install
    sudo ldconfig

Compilation takes about 70s on a Pi3 device.


Testing
-------

Use `contrib/remote_cec/test_cec.py` to test the operation of your remote.
Be sure to activate the venv that was installed together with the client.


Configuration
-------------

Copy `contrib/remote_cec/keypad_cec.py` to `src/local`. Paste the contents
of `contrib/remote_cec/hw_config_cec.py` to your `settings.py` and adapt
to your needs.
