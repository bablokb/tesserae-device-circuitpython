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
import status

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
      if isinstance(text, dict):
        print("UIProvider: {")
        for key, value in text.items():
          print(f"UIProvider:   {key}: {value}")
        print("UIProvider: }")
      else:
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

  # --- update ui   ----------------------------------------------------------

  def update_ui(self,data):
    """ update data: callback for Application """

    if data["status"] == status.NO_UPDATE:
      self.msg("no display update (status: no update)")
      return None
    if data["status"] != status.READY:
      self.msg("show user message (status: not ready)")
      return self.show_message(data["status"])

    self.msg("processing dashboard:")
    dashboard = data["dashboard"]
    if isinstance(dashboard, tuple):
      self.msg("  using bitmap from RAM")
      bitmap, ps = dashboard
    elif isinstance(dashboard, displayio.OnDiskBitmap):
      self.msg("  using bitmap from disk")
      bitmap, ps = dashboard, dashboard.pixel_shader
    else:
      self.msg("  using pygame-surface")
      self._view.surface = dashboard
      return self._view

    if len(self._view):
      self._view[0].bitmap = bitmap      # replace existing bitmap
      gc.collect()
    else:
      self._view.append(displayio.TileGrid(bitmap, pixel_shader=ps))
    return self._view

  # --- clear UI and free memory   -------------------------------------------

  def clear_ui(self):
    """ clear UI """

    if self._view:
      for _ in range(len(self._view)):
        self._view.pop()
    self._view = None
    gc.collect()

  # --- show message to the user   -------------------------------------------

  def show_message(self, status):
    """ update display with message """

    import locale, builtins
    lang = locale.getlocale()[0]
    try:
      lang_file = f"lang_{lang}"
      lang_module = builtins.__import__(lang_file,None,None,["MSG_TABLE"],0)
    except:
      # fall back to en_US
      lang_file = f"lang_en_US"
      lang_module = builtins.__import__(lang_file,None,None,["MSG_TABLE"],0)
    self.msg(f"loaded messages from {lang_file}.py")

    try:
      msg_text = lang_module.MSG_TABLE[status]
    except:
      msg_text = f"unsupported status '{status}' for language '{lang}'"

    scale = 2 if self._display.width > 479 else 1
    msg_label = label.Label(
      terminalio.FONT,
      text=msg_text,
      color=UI_PALETTE[COLOR.WHITE],
      line_spacing=1.2,
      scale=scale,
      anchor_point=(0.5,0.5),
      anchored_position=(self._display.width//2, self._display.height//2)
      )
    g = displayio.Group()
    g.append(msg_label)
    return g
    
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
