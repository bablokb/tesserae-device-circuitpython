Configuration
=============

Overview
--------

The configuration file is the Python file `src/settings.py`. This file
must create three objects of type `Settings`:

    class Settings:
      pass

    secrets = Settings()     # WLAN credentials (only needed for real hardware)
    app_config = Settings()  # application configuration
    hw_config = Settings()   # hardware configuration

These objects will be imported by other parts of the application.


Reference
---------

The detailed reference for `secrets` and `hw_config`, is in the [base
app
documentation](https://github.com/bablokb/circuitpython-base-app/config-reference-md).

The reference for application specific configuration is
[here](./docs/app_config.md).

The next sections give some typical examples. These should serve as a
blueprint for your own configuration.

For devboards with builtin hardware, it makes more sense to create a
hardware abstraction layer file (HAL) instead of using settings from
`hw_config`. HALs are distributed with the
[base-application](https://github.com/bablokb/circuitpython-base-app)
and can be reused across different applications.

Otherwise, `hw_config` needs at least three attributes:

  - `gamut`
  - `eink`
  - `get_display`

See the examples below and the files in the [contrib
directory](../contrib/Readme.md).


Examples
========

  - [Minimal Example](#minimal-example)
  - [Template Example](#template-example)
  - [External Display](#mcu-with-an-external-busdisplay)
  - [Low Memory Systems (SD caching)](#low-memory-systems)


Minimal Example
---------------

This is a minimal example, that will work with a board with integrated
display (i.e. the `board`-module has a `board.DISPLAY`-attribute:

    class Settings:
      pass

    # credentials
    secrets = Settings()
    secrets.ssid      = 'my-ssid'
    secrets.password  = 'my-secret-password'

    # application configuration
    app_config = Settings()
    app_config.url = "http://tesserae.local:8765/
    app_config.app_name = "Tesserae-Client-1"    # for Blinka/PyGame

    # hardware configuration
    hw_config = Settings()
    hw_config.gamut = "mono" # rgb16, rgb24, acep_7colour, spectra_6, gray_4
    hw_config.eink  = True   # True|False


Template Example
----------------

The file `src/settings_template.py` is a bit more detailed. It creates
all three configuration objects.

If you drop a `my_hardware.py` into `src/local`, it will import
`hw_config` from this file. Otherwise, it will fall back to the
minimal `hw_config`-object from the previous example.

The exception is an environment based on Blinka/PyGame: here it
will create `hw_config` and `app_config`-settings that are suitable
for that runtime.


MCU With an External BusDisplay
-------------------------------

A generic MCU does not have a builtin display and therefore the
`board`-module does not have a `DISPLAY` attribute. To use such a
combination, use the hardware configuration below.

The example is for an ST7789 display, but it will work with minimal
changes for other displays with similar drivers as well.

See [`../contrib/hw_config_st7789.py`](../contrib/hw_config_st7789.py)
for the full code and
[`../contrib/hw_config_sharp400.py`](../contrib/hw_config_sharp400.py)
for a variant for the Adafruit Sharp-Display.

    import atexit
    import busio
    import displayio
    import fourwire
    from adafruit_st7789 import ST7789

    # --- basic display configuration   ----------

    WIDTH      = 320
    HEIGHT     = 240
    ROTATION   = 90
    BRIGHTNESS = 0.8
    DRIVER     = ST7789

    # --- hardware-pins   ------------------------

    SCK_PIN   = board.GP10
    MOSI_PIN  = board.GP11
    MISO_PIN  = board.GP12
    DC_PIN    = board.GP8
    RST_PIN   = board.GP15
    CS_PIN    = board.GP9
    BL_PIN    = board.GP13

    # --- atexit processing   --------------------

    def at_exit(spi):
      """ release spi """
      spi.deinit()

    # --- display-factory method   ---------------

    def _get_display(hal):
      """ create display with configured driver """

      displayio.release_displays()
      spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
      atexit.register(at_exit,spi)
      display_bus = fourwire.FourWire(
        spi, command=DC_PIN, chip_select=CS_PIN,
        reset=RST_PIN, baudrate=40_000_000
      )
      display = DRIVER(display_bus, width=WIDTH, height=HEIGHT,
                       rotation=ROTATION,
                       brightness=BRIGHTNESS, backlight_pin=BL_PIN,)
      return display

    # hardware configuration   -------------------

    class Settings:
      pass

    hw_config = Settings()
    hw_config.get_display  = _get_display
    hw_config.gamut = "rgb16"
    hw_config.eink  = False


Low Memory Systems
------------------

If the MCU does not have enough memory to hold the complete bitmap of
the dashboard in memory, caching it in the filesystem is an option.
Examples in the wild are usually a Pico-W combined with a large
display, e.g. the first generation Pimoroni Inky-Frame series.

The workflow changes from *wakeup->fetch->display->sleep->reset* to
*wakeup->fetch->save->start viewer->display->sleep->reset*. The image
viewer is a seperate program that does not initialize and use wifi and
therefore provides more memory for the display task.

Implementation note: if the dashboard is too large even in viewer-mode,
the update falls back to using `OnDiskBitmap`. This is very slow
(e.g. Pico-W with 320x280 LCD: 75s), but should work for any size
of display.

Since the main filesystem of CircuitPython is normally not writable,
this typically needs an available SD-breakout for the file cache (but
see below for alternatives).

To configure the system for caching, do the following:

  1. Remove all wifi credentials (if any) from your `settings.toml`
     on the device. This will prevent that the system loads the wifi-stack.
  2. Add `CIRCUITPY_SDCARD_USB = false` to your `settings.toml`. This
     will prevent that the mounted SD card is presented to the host.
     Otherwise, the host will flood the device with USB-traffic for
     about 30 seconds.
  3. Add an `_init(hal)` method to your hardware configuration:

         def _init(hal):
            ...
         ...
         hw_config.init = _init

     Within `init()`, mount the SD-card. For boilerplate code, see the
     [IL0373 example](../contrib/hw_config_il0373.py) for a SD on a
     shared SPI bus and the [UC8179 example](../contrib/hw_config_uc8179.py)
     for a SD on a dedicated SPI bus.
  4. Add the following options to your application configuration:

         app_config.dl_mode = "FSCACHE"
         app_config.dl_dir  = "/sd"


Alternatives to the SD-Cache
----------------------------

There are two alternatives to the SD-cache that use normal internal flash:
either cache to a `/saves`-partition or cache to the root filesystem `/`.

The `/saves`-partition is part of the flash and created at *compile
time*. It is usually not available in stock CircuitPython firmware. To
use a `/saves`-partition, a custom build of CircuitPython is
necessary. An advantage of this partition is that it does not need to
be mounted and it is save to write to it. Without the option in (1)
above, it is also exposed read-only to the host.

Since the root-filesystem of the device is writable by the host, it is
normally not writable by a CircuitPython program.  Starting from CP
10.3.0, this can be changed with the following code fragment from
within `_init()` instead of mounting the SD-card:

    import storage
    storage.unsafe_disable_usb_drive()

To prevent filesystem corruption, make sure the CIRCUITPY-drive is not
mounted on the host. On Linux and macOS, deactivate automounting and
use a mount-copy-umount workflow to update program files. On Windows,
eject the CIRCUITPY-device after updating files.

Note that both alternatives might not work on the Pico-W, since the
free space in flash is also limited (about 200K free).
