# ----------------------------------------------------------------------------
# hw_config_inky_frame57.py: Configuration for the Pimoroni Inky-Frame 5.7"
#
# This device has it's own HAL, so this is not the complete hardware
# configuration.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_inky_frame57 import hw_config
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import board
import sdcardio
import storage

SD_CS_PIN = board.SD_CS

# --- init-method   ----------------------------------------------------------

def _init(hal):
  """ mount /sd. Uses board.SPI()  """

  try:
    sdcard = sdcardio.SDCard(board.SPI(),SD_CS_PIN)
    vfs    = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("init(): /sd mounted successfully")
  except Exception as ex:
    print(f"init(): failed to mount /sd with exception: {ex}")
    raise

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config = Settings()
hw_config.init = _init
