# ----------------------------------------------------------------------------
# hw_config_uc8179_tricolor.py: Settings for an UC8179 tri-color display.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_st7789 import hw_config
#
# This configuration is courtesy of Github user snowpie
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import atexit
import busio
import displayio
import fourwire
import board
from adafruit_uc8179 import UC8179

# --- Hardware config for SB Components Enk-Pi
# https://shop.sb-components.co.uk/products/enkpi

# This product is available with various sized e-ink displays.

# --- basic display configuration   ----------

WIDTH      = 600 # reduced resolution due to memory constraints
HEIGHT     = 240
ROTATION   = 180
DRIVER     = UC8179

# --- hardware-pins   ------------------------

SCK_PIN   = board.GP10
MOSI_PIN  = board.GP11
DC_PIN    = board.GP8
RST_PIN   = board.GP12
CS_PIN    = board.GP9
BUSY_PIN  = board.GP13

# --- atexit processing   --------------------

def at_exit(spi):
  """ release spi """
  spi.deinit()

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
hw_config.get_display  = _get_display
hw_config.gamut = "bwr_3"
hw_config.eink  = True
