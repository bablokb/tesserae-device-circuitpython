# ----------------------------------------------------------------------------
# Minimal image viewer to show cached images (UIProvider).
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import gc
import displayio
import time
import terminalio

from settings import app_config

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
      print(f"UIProvider: {text}")

  # --- create complete content   --------------------------------------------

  def create_ui(self,display):
    """ create content """

    if self._view:
      return

    # save display
    self._display = display

    # adding objects to the group is deferred until we have a bitmap
    self._view = displayio.Group()

    return

  # --- update ui   ----------------------------------------------------------

  def update_ui(self,data):
    """ update data: callback for Application """

    if not "dashboard" in data:
      return None

    dashboard = data["dashboard"]
    if isinstance(dashboard, tuple):
      bitmap, ps = dashboard
    elif isinstance(dashboard, displayio.OnDiskBitmap):
      bitmap, ps = dashboard, dashboard.pixel_shader
    else:
      ps = None

    if ps:
      if len(self._view):
        self._view[0].bitmap = bitmap      # replace existing bitmap
        gc.collect()
      else:
        self._view.append(displayio.TileGrid(bitmap, pixel_shader=ps))
    else:
      # a PyGame surface, attach it to the group
      self._view.surface = dashboard

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
                            color=UI_PALETTE[COLOR.RED],
                            line_spacing=1.2,
                            anchor_point=(0,0),
                            anchored_position=(0,0))

    g = displayio.Group()
    g.append(error_txt)
    return g
