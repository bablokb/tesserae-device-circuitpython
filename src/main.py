# ----------------------------------------------------------------------------
# Generic Tesserae Client.
#
# This client uses the REST-API to communicate with a Tesserae server.
# See https://github.com/dmellok/tesserae to learn about Tesserae.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

# --- imports   --------------------------------------------------------------

import board
import time
import atexit
import gc

from settings import app_config
from base_app.ui_application import UIApplication
from tesserae_dataprovider import DataProvider
from tesserae_uiprovider import UIProvider

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

# --- cleanup at exit   ------------------------------------------------------

def at_exit(app):
  app.at_exit()

# --- application class with overrides   --------------------------------------

class App(UIApplication):
  """ class App """
  def __init__(self,*args,**kwargs):
    super().__init__(*args, ** kwargs)

    if not hasattr(self.hal, "gamut"):
      raise ValueError("'gamut' not defined in hw_config")
    if not hasattr(self.hal, "eink"):
      raise ValueError("'eink' not defined in hw_config")

    self._token = None
    self._etag  = None

    # fill in attributes needed by data and ui-provider
    self.data.update({
      "url":          app_config.url,
      "name":         getattr(app_config,"name", board.board_id),
      "device_id":    app_config.device_id,
      "pairing_code": getattr(app_config,"pairing_code", None),
      "mac":          getattr(app_config,"mac", self.wifi.mac_address),
      "width":        self.display.width,
      "height":       self.display.height,
      "format":       getattr(app_config,"format", "bmp"),
      "gamut":        self.hal.gamut,
      "eink":         self.hal.eink,
      "dashboard":    self._alloc_bitmap(),
      })

  # --- override idle-processing   --------------------------------------------

  def run_idle(self):
    """ Overriden to honor sleep_time set by data-provider """
    if "sleep_time" in self.data:
      interval = self.data["sleep_time"]
    else:
      # application default run-interval
      interval = getattr(app_config, "run_interval", 60)

    self.msg(f"running idle for {interval}s")
    while time.monotonic()-self._run_start < interval:
      if self.process_events():
        return

  # --- run at start of run()   ----------------------------------------------

  def run_start(self):
    """ Hook to execute at start of run() """

    if self._token and self._etag:
      self.msg("not reading NVRAM (have token and etag)")
      # This happens when running in a loop, so don't update on 304.
      self.data["304update"] = False
      return

    # This is POR, so read data ...
    self._read_nvram()
    # ... and force updates for normal displays or in case no etag exists
    self.data.update({
      "token":        self._token,
      "etag":         self._etag,
      "304update":    not self.hal.eink or not self._etag
      })

  # --- run at end of run()   ------------------------------------------------

  def run_end(self):
    """ Hook to execute at end of run(): save token """
    self._write_nvram()
    s_time = self.data.get("server_time", None)
    if s_time:
      self.msg(f"updating RTCs")
      self.hal.update_rtc(s_time)
      now = time.localtime()
      self.msg("now: %04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday,
        now.tm_hour, now.tm_min, now.tm_sec
      ))

  # --- read persisted data   ------------------------------------------------

  def _read_nvram(self):
    """ get token and etag from NVRAM """

    if hasattr(app_config,"token"):
      # use hard coded token
      self.msg(f"using hard-coded token: {app_config.token}")
      self._token = app_config.token
    else:
      self._token = None

    self._magic = getattr(app_config, "magic", 0x4201)
    self.msg(f"reading data from NVRAM with magic: {self._magic}")
    buffer = self.hal.nvram_read(0, 3)
    if not self._magic == int(buffer[:2].hex(),16):
      # magic number does not match, invalidate token
      self.msg("magic number does not match, no data read")
      self._etag = None
      return

    # read token with given length
    if not self._token:
      # read token
      self._token = self.hal.nvram_read(3, buffer[2]).decode()
      self.msg(f"token read from NVRAM: {self._token}")
    offset = 3 + buffer[2]
    len_etag = self.hal.nvram_read(offset, 1)[0]
    self.msg(f"{len_etag=}")
    if len_etag:
      try:
        self._etag = self.hal.nvram_read(offset+1, len_etag).decode()
        self.msg(f"etag read from NVRAM: {self._etag}")
      except:
        self._etag = None
        self.msg("no valid etag in NVRAM")
    else:
      self._etag = None
      self.msg("no saved etag in NVRAM")

  # --- persist token and etag   ---------------------------------------------

  def _write_nvram(self):
    """ save token and etag

    The data is saved in NVRAM as:
      magic-number,length,token,length,etag
    The magic-number allows to verify that we don't read  random garbage
    and it allows to invalidate an old token.
    """

    if (self.data["token"] == self._token and
        self.data["etag"] == self._etag):
      # no new data, nothing to save
      self.msg("not saving data (no change)")
      return
    elif self.data["token"] == None:
      # dataprovider invalidated the token, clear magic-number
      self.msg(f"token invalidated, clearing NVRAM")
      self.hal.nvram_write(0, b'\x00\x00')
      return

    # write data to NVRAM
    self._token = self.data["token"]
    self._etag  = self.data["etag"]
    token = bytes(self.data["token"],'utf-8')
    if self._etag:
      etag = bytes(self.data["etag"],'utf-8')
    else:
      etag = ""
    buffer = bytearray(4 + len(token) + len(etag))
    offset = 0
    buffer[offset:2] = self._magic.to_bytes(2,'big'); offset += 2
    buffer[offset]  = len(token); offset += 1
    buffer[offset:offset+len(token)] = token; offset += len(token)
    buffer[offset]  = len(etag); offset += 1
    if len(etag):
      buffer[offset:offset+len(etag)] = etag
    self.msg(f"saving '{buffer}' to NVRAM")
    self.hal.nvram_write(0, buffer)

  # --- allocate a bitmap for the display   ----------------------------------

  def _alloc_bitmap(self):
    """ pre allocate a suitable bitmap """

    from displayio import Bitmap
    col_map = {
      "mono":  2,
      "gray_4": 4,
      "bwr_3":  4,
      "bwy_3":  4,
      "spectra_6":  6,
      "acep_7colour":  7,
      "rgb16": 65535,
      "rgb24": 65535,
      }
    self.msg(
      "creating Bitmap for display with" +
      f"{self.display.width}x{self.display.height}@{col_map[self.hal.gamut]}")
    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory before Bitmap allocation: {gc.mem_free()}")
    return (Bitmap(self.display.width,
                             self.display.height,
                             col_map[self.hal.gamut]),
            None)
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory after Bitmap allocation: {gc.mem_free()}")

# --- main program   ---------------------------------------------------------

if getattr(app_config,"debug",False):
  wait_for_console()

start = time.monotonic()
data_provider = DataProvider()
ui_provider = UIProvider()

app = App(data_provider,ui_provider)
atexit.register(at_exit,app)

if getattr(app_config,"debug",False):
  app.msg(f"startup: {time.monotonic()-start:f}s")

if not getattr(app_config,"always_on",False):
  app.msg(f"running once")
  app.run_once()
else:
  app.msg(f"runing endless")
  while True:
    app.run()
