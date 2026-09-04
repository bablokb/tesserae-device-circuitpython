MCU Installation
================


  0. Install the current version of CircuitPython to your device. After
     installation, you should see a new drive appearing (label "CIRCUITPY"),
     unless the device does not support native USB (e.g. ESP32/ESP32-Cx devices).
     In the latter case, follow the CircuitPython docs to access the system
     via "web-workflow". The next steps only cover the standard case, i.e.
     a device with native USB (e.g. RP2xx, ESP32-Sx).

  1. Install the following libraries from the CircuitPython library-bundle to
     the `lib`-directory of your device  

       - adafruit_display_text
       - adafruit_requests
       - a suitable driver library for your display (unless it is builtin)
       - additional libraries for your hardware setup

     The preferred way to do this is to use `circup` (note that the device
     must be mounted):  

         pip3 install circup
         circup --path /mountpoint/of/device install -r requirements.txt
         circup --path /mountpoint/of/device install adafruit_st7789

     The first circup command installs the libraries listed above, the second
     is an example for installing the ST7789 driver library.

  2. Clone the repository recursively:

        git clone --recurse-submodules \
                  https://github.com/bablokb/tesserae-device-circuitpython
        cd tesserae-device-circuitpython

  3. Copy `src/settings_template.py` to `src/settings.py` and adapt to
     your needs. Make sure to read the [configuration
     guide](./docs/configuration.md).

  4. Copy the *content* of the `src/`-directory to your device. Don't
     copy the `src` directory itself (note: *the trailing slash is
     important in the command given below!*).  
     Make sure that your copy-command does not copy the existing symlinks,
     but the directories and files they point to. Both `rsync` and `cp`
     have the option `-L` that support this operation:

         rsync -avL src/ /mountpoint/of/device

  5. Delete an existing `code.py` from the device. The default `code.py`
     from a fresh CircuitPython install shadows the `main.py`.
