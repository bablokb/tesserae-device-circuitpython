#!/bin/bash

sudo apt-get -y install swig python3-dev
sudo apt-get -y install python3-pygame python3-rpi.gpio libsdl2-2.0 \
                        libegl1 libgl1 libgl1-mesa-dri
python3 -m venv --system-site-packages "$HOME/venv.tesserae.cp-client"
. "$HOME/venv.tesserae.cp-client/bin/activate"
pip install blinka-displayio-pygamedisplay
pip install adafruit-circuitpython-display-text
