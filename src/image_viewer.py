# ----------------------------------------------------------------------------
# Minimal image viewer to show cached images.
#
# This is a companion program to main.py if files are locally cached.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

# --- imports   --------------------------------------------------------------

import time
import atexit

from settings import app_config
from base_app.ui_application import UIApplication
from iv_dataprovider import DataProvider
from iv_uiprovider import UIProvider

# --- wait for connected console   -------------------------------------------

def wait_for_console(duration=5):
  """ wait for serial connection.
  If there is no supervisor, we are on CPython and don't have to wait.
  """
  import board
  try:
    import supervisor
    import time
    elapsed = time.monotonic() + duration
    while (not supervisor.runtime.serial_connected and
           time.monotonic() < elapsed):
      time.sleep(1)
  except:
    pass
  print(f"running on board {board.board_id}")

# --- cleanup at exit   ------------------------------------------------------

def at_exit(app):
  app.at_exit()

# --- application class with overrides   -------------------------------------

class App(UIApplication):
  """ class App """
  def __init__(self,*args,**kwargs):
    super().__init__(*args, ** kwargs)

    # fill in attributes needed by data and ui-provider
    self.data.update({
      "is_pygame":          self.is_pygame,
      "dashboard_filename": self._get_filename(),
      })

  # --- query filename of downloaded dashboard   -----------------------------

  def _get_filename(self):
    """ query filename of downloaded dashboard """

    if self.is_pygame:
      dl_dir = getattr(app_config, "dl_dir", self.hal.get_appdir())
    else:
      dl_dir = getattr(app_config, "dl_dir", "/")

    # check if filename exists
    import os
    try:
      filename = None
      files = os.listdir(dl_dir)
      for f in files:
        if f.startswith("dashboard."):
          filename = f"{dl_dir}/{f}"
          self.msg(f"using filename: {filename}")
          return filename
    except OSError:
      raise ValueError(
        f"error: Invalid dl_dir configuration. {dl_dir} does not exist")

# --- main program   ---------------------------------------------------------

if getattr(app_config,"debug",False):
  wait_for_console()

start = time.monotonic()
data_provider = DataProvider()
ui_provider = UIProvider()

app = App(data_provider, ui_provider,
          with_rtc=True, with_wifi=False)
atexit.register(at_exit,app)

if getattr(app_config,"debug",False):
  print(f"startup: {time.monotonic()-start:f}s")

app.run_once()
