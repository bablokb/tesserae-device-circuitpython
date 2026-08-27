# ----------------------------------------------------------------------------
# pygame_display_info.py: name, size, gamut and MAC-address for
#                         (emulated) display types.
#
# This file is imported by src/settings_pygame.py
#
# To override, copy this file to src/local and adapt to your needs.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

# PyGame displays for appliances and emulation
# Every entry is a tuple of (width, height, gamut, MAC-address)
# (width,height) == (0,0) will use fullscreen mode
# An unset MAC-address will try to use the hardware MAC

# MAC-OUI (locally administered, unicast): int(b'TES'.hex(),16) | 0b10 << 16
MAC_OUI = "56:45:53"

PYGAME_DISPLAYS = {
  # fullscreen mode typically is appliance mode, so use hardware MAC
  "fullscreen":     (  0,   0, "rgb16", None),
  "fullscreen90":   (  0,   0, "rgb16", None),
  "fullscreen270":  (  0,   0, "rgb16", None),

  # Pimoroni Inky-Impression and Inky-Frame
  "ii4_old":     (640, 400, "acep_7colour", f"{MAC_OUI}:AD:BE:E0"),
  "ii4":         (600, 400, "spectra_6",    f"{MAC_OUI}:AD:BE:E1"),
  "ii5.7_old":   (600, 448, "acep_7colour", f"{MAC_OUI}:AD:BE:E2"),
  "ii5.7":       (600, 448, "spectra_6",    f"{MAC_OUI}:AD:BE:E3"),
  "ii7.3_old":   (800, 480, "acep_7colour", f"{MAC_OUI}:AD:BE:E4"),
  "ii7.3":       (800, 480, "spectra_6",    f"{MAC_OUI}:AD:BE:E5"),
  "iframe5.7":   (600, 448, "acep_7colour", f"{MAC_OUI}:AD:BE:E6"),

  # various other boards/displays
  "badger2040w": (296, 128, "mono",         f"{MAC_OUI}:AD:BE:E7"),
  "magtag":      (296, 128, "gray_4",       f"{MAC_OUI}:AD:BE:E8"),
  "sunton-2424": (240, 240, "rgb16",        f"{MAC_OUI}:AD:BE:E9"),
  "sharp400":    (400, 240, "mono",         f"{MAC_OUI}:AD:BE:EA"),
  "native":      (900, 600, "rgb16",        f"{MAC_OUI}:AD:BE:EB"),
  "native600":   (600, 400, "rgb16",        f"{MAC_OUI}:AD:BE:EC" ),
  "what":        (400, 300, "mono",         f"{MAC_OUI}:AD:BE:EF"),

  # Pi Touch-Display-2
  # This is for emulation only, real hardware should use
  # fullscreen, fullscreen90/fullscreen270 instead
  "pi_touch2_5P":  ( 720, 1280, "rgb16", f"{MAC_OUI}:AD:BE:A0"),
  "pi_touch2_5L":  (1280,  720, "rgb16", f"{MAC_OUI}:AD:BE:A1"),
  "pi_touch2_7P":  ( 720, 1280, "rgb16", f"{MAC_OUI}:AD:BE:A2"),
  "pi_touch2_7L":  (1280,  720, "rgb16", f"{MAC_OUI}:AD:BE:A3"),
  "pi_touch2_10P": (1200, 1920, "rgb16", f"{MAC_OUI}:AD:BE:A4"),
  "pi_touch2_10L": (1920, 1200, "rgb16", f"{MAC_OUI}:AD:BE:A5"),
}

if __name__ == "__main__":
  for key, value in PYGAME_DISPLAYS.items():
    print(f"{key:15s}: {value}")
