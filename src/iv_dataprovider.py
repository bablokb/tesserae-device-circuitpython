# ----------------------------------------------------------------------------
# Minimal image viewer to show cached images (DataProvider).
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import gc
import time

from settings import app_config

# --- main data-provider class   ---------------------------------------------

class DataProvider:

  def __init__(self):
    self._debug = getattr(app_config, "debug", False)
    self._wifi  = None

  # --- print debug-message   ------------------------------------------------

  def msg(self,text):
    """ print (debug) message """
    if self._debug:
      print(f"DataProvider: {text}")

  # --- set wifi-object   ----------------------------------------------------

  def set_wifi(self,wifi):
    """ set wifi-object (unused) """
    self._wifi = wifi

  # --- query departures   ---------------------------------------------------

  def update_data(self,data):
    """ callback for App: query data and update data-object """

    filename = data["dashboard_filename"]
    if filename is None:
      data.pop("dashboard")
      return

    # read the requested sleep-time
    with open(f'{filename}.txt','rt') as f:
      data["wake_time"] = int(f.readline())

    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory before imageload: {gc.mem_free()}")

    # create PyGame surface if requested
    start = time.monotonic()
    if data.get("is_pygame", False):
      self.msg("creating PyGame-surface from image file")
      import pygame
      data["dashboard"] = pygame.image.load(filename).convert()
      self.msg(f"pygame.image.load(): {time.monotonic()-start:0.1f}s")
    else:
      if gc.mem_free() > data["memory_requirement"]:
        self.msg("creating Bitmap from image file")
        import imageload
        data["dashboard"] = imageload.load(filename)
      else:
        self.msg("creating OnDiskBitmap from image file")
        import displayio
        data["dashboard"] = displayio.OnDiskBitmap(filename)
    self.msg(f"imageload.load(): {time.monotonic()-start:0.1f}s")

    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory after imageload: {gc.mem_free()}")
