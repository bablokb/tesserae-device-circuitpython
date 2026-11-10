# ----------------------------------------------------------------------------
# hw_config_cec.py: Configuration for CEC support.
#
# Note that CEC support is only available for Pi appliances connected to a
# TV set.
#
# This file only provides a snippet to add to your hardware-configuration.
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

# This is not a complete hw_config! Add this snippet to your settings.py!

import cec
from local import keypad_cec

# --- factory method for the keypad   ----------------------------------------

def _get_keypad(hal):
  """ return configured keypad. """
  if hal.BUTTONS and hal._display:
    return keypad_cec.CECKeys(hal.BUTTONS[0], log=hal.log)
  return None

# --- adapt hardware configuration   -----------------------------------------

hw_config.get_keypad = _get_keypad
hw_config.BUTTONS = (
  [cec.CEC_USER_CONTROL_CODE_LEFT,
   cec.CEC_USER_CONTROL_CODE_RIGHT,
   cec.CEC_USER_CONTROL_CODE_SELECT,
   cec.CEC_USER_CONTROL_CODE_F2_RED,
   cec.CEC_USER_CONTROL_CODE_F3_GREEN,
   cec.CEC_USER_CONTROL_CODE_F4_YELLOW,
   cec.CEC_USER_CONTROL_CODE_F1_BLUE,
   ], True, True)
hw_config.button_names = ["left", "right", "select",
                          "red",  "green", "yellow", "blue",
                          ]

# map application names to buttons
app_config.button_names = ["left", "right", "refresh",
                          "A",  "B", "C", "D",
                          ]
