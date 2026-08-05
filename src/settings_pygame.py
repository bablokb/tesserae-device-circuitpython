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
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay


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

# display-sizes: tuple of (width,height,gamut)

DISPLAY_TYPES = {
  "fullscreen":  (  0,   0, "rgb16"),
  "native":      (900, 600, "rgb24"),
  "native600":   (600, 400, "rgb16"),
  "what":        (400, 300, "mono"),
  "ii4_old":     (640, 400, "acep_7colour"),
  "ii4":         (600, 400, "spectra_6"),
  "ii5.7_old":   (600, 448, "acep_7colour"),
  "ii5.7":       (600, 448, "spectra_6"),
  "ii7.3_old":   (800, 480, "acep_7colour"),
  "ii7.3":       (800, 480, "spectra_6"),
  "iframe5.7":   (600, 448, "acep_7colour"),
  "badger2040w": (296, 128, "mono"),
  "magtag":      (296, 128, "gray_4"),
  "sunton-2424": (240, 240, "rgb16"),
  "sharp400":    (400, 240, "mono"),
  }

disp_type = os.getenv("TESSERAE_DISPLAY", default="native")
if disp_type in DISPLAY_TYPES:
  width, height, gamut  = DISPLAY_TYPES[disp_type]
else:
  # try to parse disp_type
  width, height, gamut = disp_type.split(',')
  width = int(width)
  height = int(height)

if disp_type == "fullscreen" or (width == 0 and height == 0):
  flags = pygame.FULLSCREEN
else:
  flags = 0

CAPTION = "Tesserae-Client"

class Settings:
  pass

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

# hardware configuration   ---------------------------------------------------

hw_config = Settings()
hw_config.get_display = _get_display
hw_config.gamut = gamut
hw_config.eink  = False
