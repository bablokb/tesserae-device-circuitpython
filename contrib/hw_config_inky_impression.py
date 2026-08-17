# ----------------------------------------------------------------------------
# hw_config_inky_impression.py: Hardware-settings specific to Pimoroni
#                               Inky-Impression displays.
#
# Merge with your settings.py or copy to src/local, adapt and use:
#
#    from local.hw_config_inky_impression import hw_config
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import struct
import displayio
import fourwire

# these pin names are Pi-Pico adapter specific and need to be adapted.
SCK_PIN   = board.SCLK
MOSI_PIN  = board.MOSI
MISO_PIN  = board.MISO
DC_PIN    = board.GPIO22
RST_PIN   = board.GPIO27
CS_PIN    = board.CE0
BUSY_PIN  = board.GPIO17
BTN_PINS  = [board.GPIO5, board.GPIO6, board.GPIO16, board.GPIO24]
LED_PIN   = board.GP14

# --- helper-function for Inky-displays   ------------------------------------

def _get_inky_info():
  """ try to return tuple (width,height,color) """
  COLOR = [None, 'black', 'red', 'yellow', None, 'acep7', 'e673', 'el133']

  EE_ADDR = 0x50
  i2c_device = I2CDevice(board.I2C(),EE_ADDR)
  buffer = bytearray(29)
  with i2c_device as i2c:
    i2c.write(bytes([0x00])+bytes([0x00]))
    i2c.write_then_readinto(bytes([0x00]),buffer)

  data = struct.unpack('<HHBBB22s',buffer)
  if data[4] == 14:
    return [data[0],data[1],'acep7']
  elif data[4] == 21:
    return [data[0],data[1],'el133']
  elif data[4] == 22:
    return [data[0],data[1],'e673']
  else:
    return [data[0],data[1],COLOR[data[2]]]

_width, _height, _inky_type = _get_inky_info()
def _get_display(hal):
  """ create display for Inky-Impression """

  displayio.release_displays()
  spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
  display_bus = fourwire.FourWire(
    spi, command=DC_PIN, chip_select=CS_PIN, reset=RST_PIN, baudrate=1000000
  )
  if _inky_type == 'acep7':
    import adafruit_spd1656
    display = adafruit_spd1656.SPD1656(display_bus,busy_pin=BUSY_PIN,
                                       width=_width,height=_height,
                                       refresh_time=28,
                                       seconds_per_frame=40)
  elif _inky_type == 'e673':
    import spectra6
    display = spectra6.Inky_673(display_bus,busy_pin=BUSY_PIN)
  else:
    raise ValueError("unsupported display")
  display.auto_refresh = False
  display.root_group = None
  return display

# hardware configuration   ---------------------------------------------------

class Settings:
  pass

hw_config             = Settings()
hw_config.LED         = LED_PIN
hw_config.BUTTONS     = [BTN_PINS, False, True]
hw_config.get_display = _get_display
hw_config.eink        = True
hw_config.gamut       = ("spectra_6" if _inky_type == 'e673' else
                         "acep_7colour")
