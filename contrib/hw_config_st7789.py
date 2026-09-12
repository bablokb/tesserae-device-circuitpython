# ----------------------------------------------------------------------------
# hw_config_st7789.py: Settings for a ST7789 based display.
#
# This specific example is for a "Waveshare Pico-ResTouch-LCD-2.8".
# The device is very picky about the SD-card.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_st7789 import hw_config
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import atexit
import board
import busio
import displayio
import fourwire
from adafruit_st7789 import ST7789

# --- basic display configuration   ------------------------------------------

WIDTH      = 320
HEIGHT     = 240
ROTATION   = 90
BRIGHTNESS = 0.8
DRIVER     = ST7789

# --- hardware-pins   --------------------------------------------------------

SCK_PIN   = board.GP10
MOSI_PIN  = board.GP11
MISO_PIN  = board.GP12
DC_PIN    = board.GP8
RST_PIN   = board.GP15
CS_PIN    = board.GP9
BL_PIN    = board.GP13
CS_SD_PIN = board.GP22

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

  # use for dl_dir="/"
  #import storage
  #storage.unsafe_disable_usb_drive()

  # use for dl_dir="/sd"
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
  """ create display with configured driver """

  display_bus = fourwire.FourWire(
    hal.spi, command=DC_PIN, chip_select=CS_PIN,
    reset=RST_PIN, baudrate=40_000_000
  )
  display = DRIVER(display_bus, width=WIDTH, height=HEIGHT,
                   rotation=ROTATION,
                   brightness=BRIGHTNESS, backlight_pin=BL_PIN,)
  return display

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config = Settings()
hw_config.init = _init
hw_config.get_display  = _get_display
hw_config.gamut = "rgb16"
hw_config.eink  = False

# all optional!
hw_config.led_blink_init = 0.1
hw_config.led_blink_power_off = 0.1
hw_config.led_blink_data = 0.0
hw_config.led_blink_exception = 0.6
