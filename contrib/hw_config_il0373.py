# ----------------------------------------------------------------------------
# hw_config_il0373.py: Settings for an IL0373 based display.
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

# --- atexit processing   ----------------------------------------------------

def at_exit(spi):
  """ release spi """
  spi.deinit()

# --- display-factory method   -----------------------------------------------

def _get_display(hal):
  """ create display with configured driver """

  displayio.release_displays()
  spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
  atexit.register(at_exit,spi)
  display_bus = fourwire.FourWire(
    spi, command=DC_PIN, chip_select=CS_PIN,
    reset=RST_PIN, baudrate=40_000_000
  )
  display = DRIVER(display_bus, width=WIDTH, height=HEIGHT,
                   rotation=ROTATION, busy_pin=BUSY_PIN, **KW_ARGS)
  return display

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config = Settings()
hw_config.get_display  = _get_display
hw_config.gamut = "bwr_3"
hw_config.eink  = True

# all optional!
hw_config.led_blink_init = 0.1
hw_config.led_blink_power_off = 0.1
hw_config.led_blink_data = 0.0
hw_config.led_blink_exception = 0.6
