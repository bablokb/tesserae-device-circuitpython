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

# network configuration (ignored for PC/laptops)   ---------------------------

secrets = Settings()
secrets.ssid      = 'my-ssid'
secrets.password  = 'my-secret-password'
secrets.retry     = 2
#secrets.debugflag = False
#secrets.channel   = 6
#secrets.timeout   = 10

# hardware configuration   ---------------------------------------------------

try:
  from local.my_hardware import hw_config
except:
  if (board.board_id == "GENERIC_LINUX_PC" or
      board.board_id.startswith("RASPBERRY_PI")):
    # this uses Blinka+PyGame on a normal Linux/macOS/Pi system
    from settings_pygame import hw_config
  else:
    # minimal (empty) hw_config for board with integrated display
    hw_config = Settings()
    hw_config.gamut = "mono" # rgb16, rgb24, acep_7colour, spectra_6, gray_4
    hw_config.eink  = True   # True|False

# app configuration   --------------------------------------------------------

# NOTE: this is the generic configuration section that works for all devices.
#       Configuration on Systems running Blinka+PyGame is more generic, see
#       the last code block in this file. The settings `name` are treated
#       differently and therefore anything
#       configured here will be overriden. So either set these values
#       there or remove the relevant lines in the last code block.

app_config = Settings()
app_config.url       = "http://tesserae.local:8765"
#app_config.name     = "Kitchen Dashboard"    # manual pretty name or
#app_config.name     = board.board_id         # use this default
app_config.debug     = False
app_config.debug_api = False
app_config.always_on = False          # use power-off or deep-sleep
#app_config.run_interval = 60         # fallback run-interval

#app_config.format   = "bmp"          # "bmp" or "png"
#app_config.rotation =                # force server-side content rotation
#app_config.mac = "02:00:00:AA:BB:CC" # override MAC autodetection
#app_config.pairing_code =            # use pairing code
#app_config.magic =                   # invalidates a stored token
#app_config.token =                   # hardwire the token

# time-table configuration: one entry for every day starting at Monday
# Format: (h_start, h_end, h_interval), (m_start, m_end, m_interval)
#         start/end are inclusive
# Note: a defined time-table will use local scheduling, otherwise
#       scheduling is based on server-side information (next_poll_s)

# This example will run Mo-Fr, 9-17 every 15 minutes
# TT_START   = 0
# TT_INT     = 15
# app_config.time_table = [
#   ((9,17,1),(TT_START,59,TT_INT)),
#   ((9,17,1),(TT_START,59,TT_INT)),
#   ((9,17,1),(TT_START,59,TT_INT)),
#   ((9,17,1),(TT_START,59,TT_INT)),
#   ((9,17,1),(TT_START,59,TT_INT)),
#   (None, None),
#   (None, None),
#   ]

# --- emulation or PyGame appliance   ----------------------------------------

# SEE NOTE ABOVE!

disp_name = os.getenv("TESSERAE_DISPLAY")
if disp_name:
  # parse name (if complete config is provided from the environment)
  disp_name = disp_name.split(',')[0]
  # put hostname in device_id and name
  import os
  hostname = os.uname()[1].split(".")[0]   # macOS reports "host.local"
  app_config.app_name  = f"Tesserae-{disp_name}"
  app_config.name      = f"{hostname} with display {disp_name}"

  # create app_config.mac only when manually configured
  if getattr(hw_config, "mac", None):
    app_config.mac = hw_config.mac

  # settings_pygame will set rotation parameter for special cases
  if hasattr(hw_config, "rotation"):
    app_config.rotation = hw_config.rotation
