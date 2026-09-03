# ----------------------------------------------------------------------------
# Dataprovider for the Generic Tesserae Client.
#
# This client uses the REST-API to communicate with a Tesserae server.
# See https://github.com/dmellok/tesserae to learn about Tesserae.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import gc
import time

from settings import app_config
from tesserae_api import Tesserae_ID, Tesserae_API
import imageload

# --- main data-provider class   ---------------------------------------------

class DataProvider:

  def __init__(self):
    self._debug = getattr(app_config, "debug", False)
    self._wifi  = None
    self._api   = None

  # --- print debug-message   ------------------------------------------------

  def msg(self,text):
    """ print (debug) message """
    if self._debug:
      if isinstance(text, dict):
        print("DataProvider: {")
        for key, value in text.items():
          print(f"DataProvider:   {key}: {value}")
        print("DataProvider: }")
      else:
        print(f"DataProvider: {text}")

  # --- set wifi-object   ----------------------------------------------------

  def set_wifi(self,wifi):
    """ callback set wifi-object """
    self._wifi = wifi

  # --- create API interface   -----------------------------------------------

  def _create_api(self):
    """ create API interface """
    self.msg("creating API-interface")
    if not self._wifi.radio.connected:
      self._wifi.connect()

    self._panel = Tesserae_ID(self._data["name"],
                              self._data["device_id"],
                              self._data["width"],
                              self._data["height"],
                              self._data["rotation"],
                              self._data["format"],
                              self._data["gamut"],
                              self._data["mac"])
    self._api   = Tesserae_API(self._panel.id,
                               self._data["url"],
                               self._wifi.requests,
                               token=self._data["token"],
                               debug=getattr(app_config, "debug_api", False))

  # --- create bitmap   ------------------------------------------------------

  def _create_bitmap(self):
    """ create a bitmap, palette """

    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory before imageload: {gc.mem_free()}")

    # reuse existing bitmap if available
    dl_mode = self._data["dl_mode"]
    if not dl_mode == "PYGAME":
      if "dashboard" in self._data:
        bitmap = self._data["dashboard"][0]
      else:
        bitmap = None

    # download to RAM or surface if required
    if dl_mode in ["PYGAME", "RAM"]:
      import io
      start = time.monotonic()
      io_obj = self._api.url_content(io_obj=io.BytesIO(bytearray(0)))
      self.msg(f"url_content(): {time.monotonic()-start:0.1f}s")

    # create PyGame surface if requested
    if dl_mode == "PYGAME":
      import pygame
      start = time.monotonic()
      self._data["dashboard"] = pygame.image.load(io_obj).convert()
      self.msg(f"pygame.image.load(): {time.monotonic()-start:0.1f}s")
      io_obj.close()

    # stream the bmp to the bitmap. main.py enforces bmp for STREAM
    elif dl_mode == "STREAM":
      response = self._api.url_content(io_obj=None)
      # adafruit_requests only supports a single request at a time,
      # so process it now before we call /status. The response
      # is closed automatically.
      self._data["dashboard"] = imageload.load(
        imageload.ResponseReader(response), bitmap)
    elif dl_mode == "RAM":
      start = time.monotonic()
      self._data["dashboard"] = imageload.load(io_obj, bitmap)
      self.msg(f"imageload.load(): {time.monotonic()-start:0.1f}s")
      io_obj.close()
    else:
      raise NotImplementedError(f"invalid download-mode {dl_mode}")

    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory after imageload: {gc.mem_free()}")
    return

  # --- discovery helper   ---------------------------------------------------

  def discover(self):
    """ use discovery """
    code, headers, resp = self._api.discover()

    # bail out (fatal errors):
    if code != 200:
      raise RuntimeError(
        f"Tesserae-Server HTTP-Code: {code}, content: {resp}")
    if headers.get("x-tesserae-device-id-changed", "false") != "false":
      if "sleep_time" in self._data:
        del self._data["sleep_time"]
      raise RuntimeError(
        f"error: duplicate MAC for device_id: {self._data['device_id']}")

    if resp.get("registered",False):
      self.msg(f"registered with token: {self._api.token}")
      self._data["token"] = self._api.token
      return 0
    else:
      self.msg("waiting for admin registration")
      return resp.get("retry_after_s",30)

  # --- register helper   --------------------------------------------------

  def register(self, pairing_code):
    """ use fallback registration """
    code, headers, resp = self._api.register(pairing_code)
    if code != 201:
      # bail out
      raise RuntimeError(f"Tesserae-Server HTTP-Code: {code}, content: {resp}")
    self._data["token"] = self._api.token
    self.msg(
      f"registered with token: {self._api.token} (reused: {resp.reused_existing}"
    )

  # --- query data   ---------------------------------------------------------

  def update_data(self,data):
    """ callback for App: query data and update data-object """

    # this data provider follows the discover/register workflow from the
    # docs.

    # save a reference to the model
    self._data = data
    # create and cache the API interface
    if not self._api:
      self._create_api()

    # skip discovery/registration if we have a token
    if not self._data["token"]:
      if self._data["pairing_code"]:
        self.register(self._data["pairing_code"])
      else:
        wait_time = self.discover()
        if wait_time:
          # not yet registered by admin
          data["sleep_time"] = wait_time
          return

    # at this point we should have a token (or the pairing code is invalid)
    data["updated"] = False
    self._api.etag = data["etag"]
    start = time.monotonic()
    code, resp = self._api.frame()
    self.msg(f"/frame: {time.monotonic()-start:0.1f}s")
    self.msg(f"api.frame(): HTTP-code: {code}")
    if resp:
      self.msg(resp)

    if code not in [200, 204, 304, 401, 403, 404]:
      raise RuntimeError(f"/frame: unexpected HTTP return code {code}")

    # if token is invalid, delete and restart
    if code in [401, 403, 404]:
      self.msg("invalid bearer token")
      self._api.token = None
      self._data["token"] = None
      data["sleep_time"] = 1

    # save etag (will be persisted by the main application)
    if code == 200:
      self.msg(f"new etag: {self._api.etag}")
      data["etag"] = self._api.etag

    # fetch dashboard data for HTTP200 and if requested
    if code == 200 or (code == 304 and data["304update"]):
      self.msg(f"fetching dashboard for HTTP-code {code}")
      start = time.monotonic()
      response = None
      try:
        self._create_bitmap()
        data["updated"] = True
      except Exception as ex:
        self.msg("failed to create bitmap from response")
        self.msg(f"  Exception: {ex}")
        raise
      finally:
        if response:
          response = None
      self.msg(f"fetch dashboard: {time.monotonic()-start:0.1f}s")

    # cleanup and log memory state
    gc.collect()
    if hasattr(gc,"mem_free"):
      self.msg(f"free memory after cleanup: {gc.mem_free()}")

    if code < 400:
      # send status (with battery information)
      start = time.monotonic()
      code, headers, resp = self._api.status(
        {"battery_mv": 1000*data["bat_level"],
         "fw_version": (f'CP client: {data["fw_version"]}/'+
                        f'CP API: {self._panel.id["fw_version"]}'),
         })
      self.msg(f"/status: {time.monotonic()-start:0.1f}s")
      self.msg(f"api.status(): HTTP-code: {code}")
      if code == 200:
        self.msg(resp)
        data["sleep_time"] = resp.get("next_poll_s",30)
        s_time = resp.get("server_time", None)
        s_off  = resp.get("tz_offset_seconds", None)
        if s_time and s_off:
          data["server_time"] = s_time + s_off
      else:
        raise RuntimeError(f"/status: unexpected HTTP return code {code}")

    return
