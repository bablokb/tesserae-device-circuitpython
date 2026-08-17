# ----------------------------------------------------------------------------
# hw_settings_sharp400.py: Settings for a Sharp Memory Display.
#
# Merge with your settings.py or copy to src/local, adapt as needed and use:
#
#    from local.hw_config_sharp400 import hw_config
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import atexit
import board
import busio
import displayio
import framebufferio
import sharpdisplay

# --- basic display configuration   ------------------------------------------

WIDTH      = 400
HEIGHT     = 240

# --- hardware-pins   --------------------------------------------------------

SCK_PIN   = board.GP2
MOSI_PIN  = board.GP3
CS_PIN    = board.GP5
LED_PIN   = board.LED

# --- atexit processing   ----------------------------------------------------

def at_exit(spi):
  """ release spi """
  spi.deinit()

# --- display-factory method   ------------------------------------------------

def _get_display(hal):
  """ create display for a Sharp Memory Display """

  displayio.release_displays()
  spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN)
  atexit.register(at_exit,spi)

  # For the 400x240 display (can only be operated at 2MHz)
  framebuffer = sharpdisplay.SharpMemoryFramebuffer(spi,CS_PIN,WIDTH,HEIGHT)
  return framebufferio.FramebufferDisplay(framebuffer, auto_refresh=False)

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config     = Settings()
hw_config.LED = LED_PIN
hw_config.get_display = _get_display
hw_config.gamut = "mono"
hw_config.eink  = False

# all optional!
hw_config.led_blink_init = 0.1
hw_config.led_blink_power_off = 0.1
hw_config.led_blink_data = 0.0
hw_config.led_blink_exception = 0.6
