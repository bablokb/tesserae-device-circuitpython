# ----------------------------------------------------------------------------
# settings_pygame.py: Hardware-settings specific to pygame. Not maintained
#                     in repo.
#
# This file is imported by src/settings.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import os
import time
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay

# --- value holder class   ---------------------------------------------------

class Settings:
  pass

# --- pygame display that keeps the window alive on macOS   ------------------

class TesseraePyGameDisplay(PyGameDisplay):
  """ PyGameDisplay variant that pumps the full SDL event queue.

  The base check_quit() only does a *filtered* pygame.event.get(), which
  does not pump the underlying (Cocoa) event queue. On macOS a window whose
  event queue is never pumped is never actually shown, so the app window
  stays invisible. Pumping here makes the window appear and stay responsive.
  """

  def check_quit(self, delay=0.05):
    pygame.event.pump()
    return super().check_quit(delay=delay)

  def _refresh_display(self):
    """ override base-class: handle PyGame surfaces directly """
    surface = getattr(self.root_group, "surface", [])
    if not isinstance(surface, list):
      surface = [surface]
    if len(surface):
      for s in surface:
        self._pygame_screen.blit(s, (0,0))
      pygame.display.flip()
      self._last_refresh = time.monotonic()
      self._refresh_pending = False
      return
    else:
      super()._refresh_display()

# --- helper-function for HAL   ----------------------------------------------

def _get_display(hal):
  """ create display for pygame
  Simulates color-depth or color-attributes according to display-type.
  """

  display = TesseraePyGameDisplay(width=width,height=height,
                                  flags=flags,
                                  caption=CAPTION,
                                  auto_refresh=True,
                                  refresh_on_pygame_events=True,
                                  native_frames_per_second=0.5)

  # pump the event queue a few times so the window is actually shown before
  # the app blocks on its first (network) update; without this macOS may
  # keep the freshly-created window hidden.
  for _ in range(3):
    pygame.event.pump()
    pygame.display.flip()
  return display

# --- MAC generator   --------------------------------------------------------

def gen_mac(s):
  """ create pseudo-MAC """
  try:
    import zlib
    smac = f"{zlib.crc32(bytes(s,'utf-8')):0x}".upper()
    return MAC_OUI+":"+":".join([smac[i:i+2] for i in range(0,6,2)])
  except:
    # give up
    return None

# --- select display from environment   --------------------------------------

try:
  # local override
  from local.pygame_display_info import PYGAME_DISPLAYS, MAC_OUI
except:
  # distribution defaults
  from pygame_display_info import PYGAME_DISPLAYS, MAC_OUI

display_info = os.getenv("TESSERAE_DISPLAY", default="native")
if display_info in PYGAME_DISPLAYS:
  # this is a pre-defined display
  width, height, gamut, mac  = PYGAME_DISPLAYS[display_info]
  display_name = display_info
else:
  # ad-hoc defined display
  # try to parse info as: (display_name[, width, height[, gamut[, mac]]])
  dinfo    = display_info.split(',')
  display_name = dinfo[0]
  width        = int(dinfo[1]) if len(dinfo) > 2 else 0
  height       = int(dinfo[2]) if len(dinfo) > 2 else 0
  gamut        = dinfo[3]      if len(dinfo) > 3 else "rgb16"
  mac          = dinfo[4]      if len(dinfo) > 4 else gen_mac(display_info)

if display_name.startswith("fullscreen") or (width == 0 and height == 0):
  flags = pygame.FULLSCREEN
else:
  flags = 0

if display_name.endswith("90"):
  rotation = 90
elif display_name.endswith("270"):
  rotation = 270
else:
  rotation = 0

CAPTION = f"Tesserae-Client ({display_name})"

# hardware configuration   ---------------------------------------------------

hw_config = Settings()
hw_config.get_display = _get_display
hw_config.gamut = gamut
hw_config.eink  = False
if mac:
  hw_config.mac   = mac
hw_config.rotation = rotation
