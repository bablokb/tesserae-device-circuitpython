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

The next sections give some typical examples. These should serve as a blueprint
for your own configuration.

Note: 

For devboards with builtin hardware, it makes more sense to create a
hardware abstraction layer file (HAL) instead of using settings from
`hw_config`. HALs are distributed with the
[base-application](https://github.com/bablokb/circuitpython-base-app)
and can be reused across different applications.


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
    app_config.device_id = "device_nr_1"
    app_config.name = "Weather Info Kitchen"
    app_config.app_name = "Tesserae-Client-1"

    # hardware configuration
    hw_config = Settings()
    hw_config.gamut = "mono" # rgb16, rgb24, acep_7colour, spectra_6, gray_4
    hw_config.eink  = True   # True|False


Template Example
----------------

The file `src/settings_template.py` is a bit more detailed. It creates
a `secrets`-object like above. If you drop a `hw_config.py` into `src/local`,
it will use this file the hardware configuration. Otherwise, it either creates
a `hw_config`-object as shown in the previous example, or an object that
is suitable for the Blinka-PyGame environment.


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
