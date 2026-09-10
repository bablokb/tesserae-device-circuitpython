# ----------------------------------------------------------------------------
# Generic Tesserae Client: status codes.
#
# These codes drive logic and user-visible messages on the display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

INITIAL     =  0  # POR or token invalidated
WAITING     =  1  # waiting for admin registration
REGISTERED  =  2  # registered
IDLE        =  3  # nothing pushed or updated
READY       =  4  # new dashboard ready for display
CACHED      =  5  # new dashboard downloaded to FSCACHE
UPDATED     =  6  # display is updated

ERR_MAC     = 32  # duplicate MAC, intervention necessary
ERR_NET     = 33  # network error (could be transient)
ERR_UNKNOWN = 34  # unknown error
