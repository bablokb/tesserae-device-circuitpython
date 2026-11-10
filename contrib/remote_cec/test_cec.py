import time
import keypad_cec
import cec

# set to True to catch all keys
ALL_KEYS = False

# create keypad
if ALL_KEYS:
  kp_keys = []
else:
  kp_keys = [cec.CEC_USER_CONTROL_CODE_LEFT,
             cec.CEC_USER_CONTROL_CODE_RIGHT,
             cec.CEC_USER_CONTROL_CODE_SELECT,
             cec.CEC_USER_CONTROL_CODE_F2_RED,
             cec.CEC_USER_CONTROL_CODE_F3_GREEN,
             cec.CEC_USER_CONTROL_CODE_F4_YELLOW,
             cec.CEC_USER_CONTROL_CODE_F1_BLUE,
             ]

kp = keypad_cec.CECKeys(kp_keys, value_when_pressed=True, interval=0.02,
                        log=print)

while True:
  event = kp.events.get()  # a keypad-event, not a pygame-event!
  if event:
    print(f"{event.key_number=}")
  time.sleep(0.2)
