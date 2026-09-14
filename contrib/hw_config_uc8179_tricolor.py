# ----------------------------------------------------------------------------
# hw_config_uc8179_tricolor.py: Settings for an UC8179 tri-color display.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_uc8179_tricolor import hw_config
#
# This configuration is courtesy of Github user snowpie
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import atexit
import board
import busio
import displayio
import fourwire
import sdcardio
import storage

from adafruit_uc8179 import UC8179

# --- Hardware config for SB Components Enk-Pi
# https://shop.sb-components.co.uk/products/enkpi

# This product is available with various sized e-ink displays.

# --- basic display configuration   ----------

WIDTH      = 800
HEIGHT     = 480
ROTATION   = 180
DRIVER     = UC8179

# --- hardware-pins   ------------------------

SCK_PIN   = board.GP10
MOSI_PIN  = board.GP11
DC_PIN    = board.GP8
RST_PIN   = board.GP12
CS_PIN    = board.GP9
BUSY_PIN  = board.GP13

SD_SCK_PIN   = board.GP18
SD_MOSI_PIN  = board.GP19
SD_MISO_PIN  = board.GP16
SD_CS_PIN    = board.GP17

# --- atexit processing   --------------------

def at_exit(spi):
  """ release spi """
  spi.deinit()

# --- init-method   ----------------------------------------------------------

def _init(hal):
  """ initialize dedicated SPI here and mount /sd if possible """

  hal = busio.SPI(SD_SCK_PIN,MOSI=SD_MOSI_PIN,MISO=SD_MISO_PIN)
  atexit.register(at_exit,hal)

  # use for dl_dir="/" (read the documentation before you use this!)
  #storage.unsafe_disable_usb_drive()

  # use for dl_dir="/sd"
  try:
    sdcard = sdcardio.SDCard(hal,SD_CS_PIN)
    vfs    = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("init(): /sd mounted successfully")
  except Exception as ex:
    print(f"init(): failed to mount /sd with exception: {ex}")
    raise

# --- display-factory method   ---------------

def _get_display(hal):
  """ create display with configured driver """

  displayio.release_displays()
  spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN)
  atexit.register(at_exit,spi)
  display_bus = fourwire.FourWire(
    spi, command=DC_PIN, chip_select=CS_PIN,
    reset=RST_PIN, baudrate=4000000
  )
  display = DRIVER(display_bus,
                   width=WIDTH, height=HEIGHT,
                   rotation=ROTATION,
                   busy_pin=BUSY_PIN,
                   black_bits_inverted=True,
                   highlight_color=0xFF0000,
                   colstart=0,)
  return display

# hardware configuration   -------------------

class Settings:
  pass

hw_config = Settings()
hw_config.init = _init
hw_config.get_display  = _get_display
hw_config.gamut = "bwr_3"
hw_config.eink  = True
# buttons are low on press, configure internal pullups
hw_config.BUTTONS = ([board.GP2, board.GP3, board.GP4,
                      board.GP5, board.GP14,board.GP15,
                      ], False, True)
