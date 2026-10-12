# ----------------------------------------------------------------------------
# Message translations for en_US.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import status

MSG_TABLE = {
  status.WAITING     : "waiting for admin registration",
  status.NO_PUSH     : "no dashboard available yet",
  status.ERR_MAC     : "duplicate MAC, intervention necessary",
  status.ERR_NET     : "network error (could be transient)",
  status.ERR_UNKNOWN : "unknown error"
  }
