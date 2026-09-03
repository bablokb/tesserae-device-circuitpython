# ----------------------------------------------------------------------------
# UI-Provider for the Generic Tesserae Client.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import gc
import displayio
import terminalio

from adafruit_display_text import label

from settings import app_config
from ui_settings import UI_PALETTE, COLOR

# --- main data-provider class   ---------------------------------------------

class UIProvider:

  def __init__(self):
    self._debug   = getattr(app_config, "debug", False)
    self._display = None
    self._view    = None

  # --- print debug-message   ------------------------------------------------

  def msg(self,text):
    """ print (debug) message """
    if self._debug:
      print(text)

  # --- create complete content   --------------------------------------------

  def create_ui(self,display):
    """ create content """

    if self._view:
      return

    # save display
    self._display = display

    # adding objects to the group is deferred until we have a bitmpa
    self._view = displayio.Group()

  # --- update ui   ----------------------------------------------------------

  def update_ui(self,data):
    """ update data: callback for Application """

    if not data.get("updated",False):
      return None

    if data["dl_mode"] == "PYGAME":
      # for a PyGame surface, attach it to the group
      self._view.surface = data["dashboard"]
    else:
      # palette could also be a ColorConverter
      bitmap, palette = data["dashboard"]
      if len(self._view):
        self._view[0].bitmap = bitmap      # replace existing bitmap
        gc.collect()
      else:
        self._view.append(displayio.TileGrid(bitmap, pixel_shader=palette))
    return self._view

  # --- clear UI and free memory   -------------------------------------------

  def clear_ui(self):
    """ clear UI """

    if self._view:
      for _ in range(len(self._view)):
        self._view.pop()
    self._view = None
    gc.collect()

  # --- handle exception   ---------------------------------------------------

  def handle_exception(self,ex):
    """ handle exception """

    import traceback
    try:
      # CircuitPython and CPython > 3.9
      ex_txt = ''.join(traceback.format_exception(ex))
    except:
      # CPython prior to 3.10
      ex_txt = ''.join(traceback.format_exception(None, ex, ex.__traceback__))

    # print to console
    print(60*'-')
    print(ex_txt)
    print(60*'-')

    # and update display
    if not self._display:
      return

    error_txt = label.Label(terminalio.FONT,
                            text=ex_txt,
                            color=UI_PALETTE[COLOR.WHITE],
                            line_spacing=1.2,
                            anchor_point=(0,0),
                            anchored_position=(0,0))

    g = displayio.Group()
    g.append(error_txt)
    return g
