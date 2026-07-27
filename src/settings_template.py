# ----------------------------------------------------------------------------
# settings_template.py: template for settings.py
#
# Copy this file to settings.py and adapt to your needs.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import os
import board

class Settings:
  pass

# hardware configuration   ---------------------------------------------------

if (board.board_id == "GENERIC_LINUX_PC" or
    board.board_id.startswith("RASPBERRY_PI")):
  # this uses Blinka+PyGame on a normal Linux/macOS/Pi system
  from settings_pygame import hw_config
else:
  # minimal (empty) hw_config for board with integrated display
  hw_config = Settings()
  hw_config.gamut = "mono" # rgb16, rgb24, acep_7colour, spectra_6, gray_4
  hw_config.eink  = True   # True|False

# network configuration (ignored for PC/laptops)   ---------------------------

secrets = Settings()
secrets.ssid      = 'my-ssid'
secrets.password  = 'my-secret-password'
secrets.retry     = 2
#secrets.debugflag = False
#secrets.channel   = 6
#secrets.timeout   = 10

# app configuration   --------------------------------------------------------

# generic
app_config = Settings()
#app_config.debug        = False
app_config.always_on    = True     # should be off when running on batteries

# application specific
app_config.url       = "http://tesserae.local:8765"
#app_config.debug_api = False
#app_config.pairing_code =         # untested
#app_config.magic =                # invalidates a stored token

# for emulation: add various settings according to display-type
#                this allows simulating multiple displays in parallel
disp_type = os.getenv("TESSERAE_DISPLAY")

if disp_type is None:
  # real hardware
  app_config.name = "CP-Client"
  #app_config.mac = ...

else:
  # emulation
  app_config.app_name  = f"Tesserae-{disp_type}"
  app_config.device_id = f"cp_{disp_type}"
  app_config.name      = f"CP-Client-{disp_type}"
  if disp_type == "ii4_old":
    # use auto-detected mac, not available on macOS
    pass
  elif disp_type == "native":
    app_config.mac = "DE:AD:BE:EF"
  elif disp_type == "sharp400":
    app_config.mac = "DE:AD:BE:EE"
