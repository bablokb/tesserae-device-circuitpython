# ----------------------------------------------------------------------------
# keypad_cec: a keypad-module compatible class that captures CEC-events.
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import keypad
import time
import cec

LOG_SRC = "CEC"
class CECKeys(keypad._KeysBase):
  # pylint: disable=too-many-instance-attributes
  """Capture CEC key presses and create events"""

  # --- constructor   --------------------------------------------------------

  def __init__(self, keys, *, value_when_pressed = None,
               pull=True, interval=0, max_events=64, log=None):
    """ constructor """
    if log:
      self.log = log
    self._scanning = True
    self._interval = interval
    self._keycodes = keys
    self._value_when_pressed = value_when_pressed
    self._last_scan = time.monotonic()
    self._currently_pressed = [False] * self.key_count
    self._previously_pressed = [False] * self.key_count

    # create CEC configuration and interface
    self._cec_loglevel = cec.CEC_LOG_WARNING
    self._cecconfig = cec.libcec_configuration()
    self._cecconfig.strDeviceName   = "TesseraeClient"
    self._cecconfig.bActivateSource = 0
    self._cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
    self._cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT
    self._cecconfig.SetLogCallback(self._cec_log_callback)
    self._cecconfig.SetKeyPressCallback(self._cec_key_callback)
    self._cec = cec.ICECAdapter.Create(self._cecconfig)
    self.log(LOG_SRC,"libCEC version: " +
             f"{self._cec.VersionToString(self._cecconfig.serverVersion)}")
    self.log(LOG_SRC,f"libCEC info: {self._cec.GetLibInfo()}")

    # search for adapters
    adapter = self._get_com_port()
    if adapter == None:
      self.log(LOG_SRC, "No CEC adapters found")
    elif self._cec.Open(adapter):
      self.log(LOG_SRC, "CEC connection opened")
      #self._cec.SetActiveSource()
    else:
      self.log(LOG_SRC, "failed to open a connection to the CEC adapter")

    super().__init__(interval, max_events, self._keypad_keys_scan)

  # --- detect an adapter and return the com port path   ----------------------

  def _get_com_port(self):
    retval = None
    adapters = self._cec.DetectAdapters()
    for adapter in adapters:
      self.log(LOG_SRC, "found a CEC adapter:")
      self.log(LOG_SRC, "port:     " + adapter.strComName)
      self.log(LOG_SRC, "vendor:   " + hex(adapter.iVendorId))
      self.log(LOG_SRC, "product:  " + hex(adapter.iProductId))
      retval = adapter.strComName
    return retval

  # --- process log-messages   ------------------------------------------------
  
  def _cec_log_callback(self, level, time, message):
    """ process log messages (just send them to debug-output) """
    if level > self._cec_loglevel:
      return 0

    if level == cec.CEC_LOG_ERROR:
      ceclevel = "CEC-ERROR: "
      levelstr = "ERROR"
    elif level == cec.CEC_LOG_WARNING:
      ceclevel = "CEC-WARNING: "
      levelstr = "WARN"
    elif level == cec.CEC_LOG_NOTICE:
      ceclevel = "CEC-NOTICE: "
      levelstr = "INFO"
    elif level == cec.CEC_LOG_TRAFFIC:
      ceclevel = "CEC-TRAFFIC: "
      levelstr = "TRACE"
    elif level == cec.CEC_LOG_DEBUG:
      ceclevel = "CEC-DEBUG: "
      levelstr = "DEBUG"

    self.log(LOG_SRC, levelstr, ceclevel + "[" + str(time) + "]     " + message)
    return 0

  # --- print debug-message   ------------------------------------------------

  def log(self, src, *args):
    """ print (debug) message. Override from application """
    pass

  # --- deinit and close adapter   -------------------------------------------

  def deinit(self):
    """Stop scanning"""
    self._scanning = False
    self._cec.Close()
    super().deinit()

  # --- reset internal state   -----------------------------------------------

  def reset(self):
    """Reset the internal state of the scanner"""

  # --- return number of keys that are scanned   -----------------------------

  @property
  def key_count(self):
    """The number of keys that are being scanned. (read-only)"""
    return len(self._keycodes)

  # --- scanning loop (noop)   -----------------------------------------------

  def _scanning_loop(self):
    """This is called in a thread.
    Use a no-op implementation, since CEC uses a direct callback.
    """
    while self._scanning:
      time.sleep(self._interval)

  # --- scan keys from scanning-loop (never called)   ------------------------

  def _keypad_keys_scan(self):
    """Never called, since we override _scanning_loop"""

  # --- callback from libcec   -----------------------------------------------

  def _cec_key_callback(self, key, duration):
    """Check the given event for a key in our list.
    This method is called from a background CEC thread"""

    self.log(LOG_SRC, f"_cec_callback(): {key=}, {duration=}")

    # these are duplicates?!
    if not duration:
      return
    elapsed = time.monotonic() - self._last_scan
    if self._interval - elapsed > 0:
      # simulate _scanning_loop: every self._interval
      return
    self._last_scan = time.monotonic()
    # check keys (record all keys if list of keys is empty)
    keys = (
        enumerate(self._keycodes)
        if self._keycodes
        else [(key, key)]
    )
    for key_number, keycode in keys:
      if key == keycode:
        # second parameter is boolean, using this for duration
        self._events.keypad_eventqueue_record(key_number, duration)
        return
    self.log(LOG_SRC, f"_cec_callback(): ignoring {key=}")
    return
