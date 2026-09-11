# ----------------------------------------------------------------------------
# hw_config_il0373.py: Settings for an IL0373 based display.
#
# Note that the specific display (Adafruit tri-color 1.54" 152x152)
# does not need to cache images on a SD. But this example demonstrates
# how to create and use a shared SPI-bus and to mount the SD.
#
# In case the mount fails (typically because of a missing SD) nothing
# happens: the app might not use the SD after all. Depending on the
# requirements, it might be better to re-raise the exception.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_il0373 import hw_config
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import atexit
import board
import busio
import displayio
import fourwire
from adafruit_il0373 import IL0373

# --- basic display configuration   ------------------------------------------

# not every display supports every options, e.g. some are grayscale and
# need grayscale=True instead of highlight_color=0xFF0000.

WIDTH      = 152
HEIGHT     = 152
ROTATION   = 180
DRIVER     = IL0373
KW_ARGS    = {"highlight_color": 0xFF0000,
              "swap_rams": False,
              "black_bits_inverted": False,
              "color_bits_inverted": True}

# --- hardware-pins   --------------------------------------------------------

SCK_PIN   = board.GP10
MOSI_PIN  = board.GP11
MISO_PIN  = board.GP12
DC_PIN    = board.GP8
RST_PIN   = board.GP15
CS_PIN    = board.GP9
BUSY_PIN  = board.GP13
CS_SD_PIN = board.GP14

# --- atexit processing   ----------------------------------------------------

def at_exit(spi):
  """ release spi """
  spi.deinit()

# --- init-method   ----------------------------------------------------------

def _init(hal):
  """ initialize shared SPI here and mount /sd if possible """

  displayio.release_displays()
  hal.spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
  atexit.register(at_exit,hal.spi)

  try:
    import sdcardio
    import storage
    sdcard = sdcardio.SDCard(hal.spi,CS_SD_PIN)
    vfs    = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("init(): /sd mounted successfully")
  except Exception as ex:
    print(f"init(): failed to mount /sd with exception: {ex}")

# --- display-factory method   -----------------------------------------------

def _get_display(hal):
  """ create display with configured driver.
  This reuses the shared SPI created in init().
  """

  display_bus = fourwire.FourWire(
    hal.spi, command=DC_PIN, chip_select=CS_PIN,
    reset=RST_PIN, baudrate=40_000_000
  )
  display = DRIVER(display_bus, width=WIDTH, height=HEIGHT,
                   rotation=ROTATION, busy_pin=BUSY_PIN, **KW_ARGS)
  return display

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config = Settings()
hw_config.init = _init
hw_config.get_display  = _get_display
hw_config.gamut = "bwr_3"
hw_config.eink  = True

# all optional!
hw_config.led_blink_init = 0.1
hw_config.led_blink_power_off = 0.1
hw_config.led_blink_data = 0.0
hw_config.led_blink_exception = 0.6
