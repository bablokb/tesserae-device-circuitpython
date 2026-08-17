Application Configuration
=========================

Overview
--------

All application settings are attributes of a value-holder class. A minimal
example would be:

    class Settings():
      pass
    app_config = Settings()
    app_config.url = "http://tesserae.local:8765/
    app_config.device_id = "device_nr_1"
    app_config.name = "Weather Info Kitchen"
    app_config.app_name = "Tesserae-Client-1"

The following table documents existing settings. Only a subset is
necessary, since sensible defaults exist. For details about individual
settings, see the sections below.

| Attribute      | Type    | Mand. | Def.   | Description                 |
|----------------|---------|-------|--------|-----------------------------|
| url            | str     | yes   |        | URL of Tesserae-server      |
| device_id      | str     | yes   |        | Technical ID of device      |
| name           | str     | no    | ¹      | Pretty Name of device       |
| mac            | str     | no    |        | MAC-address as hex-string   |
| format         | str     | no    | "bmp"  | dashboard image format      |
| rotation       | int     | no    | 0      | one of 0, 90, 180, 270      |
| token          | str     | no    |        | Token code                  | 
| pairing_code   | str     | no    |        | Pairing code                |
| magic          | int     | no    | 0x4101 | Magic number                |
| always_on      | bool    | no    | False  | Run in a loop               |
| debug          | bool    | no    | False  | Verbose app messages        |
| debug_api      | bool    | no    | False  | Verbose API operation       |
| app_name       | str     | yes²  |        | Local application name      |
| run_interval   | int     | no    | 60     | Fallback interval           | 
| time_table     | list    | no    |        | Local scheduling            |

¹ The name defaults to `board.board_id`
² Mandatory only for PyGame-Blinka based systems


url
---

The URL of the Tesserae server.


device_id
---------

This is the technical id of a device within Tesserae. No special
characters (e.g. spaces) are allowed.


name
----

The pretty name of a device. Defaults to `board.board_id`.


mac
---

The MAC-address is usually auto detected. If not, set it explicitely.


format
------

The binary format of dashboards images. Currently only `bmp` is supported.
Support for `png` is planned.


rotation
--------

This setting requests content rotation on server side before delivery
to the client. Don't confuse this with the `rotation=` parameter of
CircuitPython display-classes. The latter is necessary for the low-level
driver to rotate content to match physical dimensions of the hardware.

`app_config.rotation` is necessary for

  - boards with builtin displays that are not used in the default ("natural")
    orientation, e.g. a Pimoroni Inky-Frame in portrait mode.
  - a Pi5 lite-system with a Pi-Touch-Display-2. These displays are always
    identified as portrait. If used in landscape mode, set the rotation
    value to `90` or `270`.


token
-----

Hard-coded device token as provided during discovery and registration. Since
the token is usually saved in NVRAM, it recommended to never use this
attribute.


pairing_code
------------

This code is for one-time use during the alternative registration path. See
the Tesserae documentation for details.


magic
-----

Magic-number for NVRAM access. This is a two-byte integer that
validates the NVRAM does not contain garbage. Changing this value will
restart the registration process at next start.

This attribute should usually be left at its default value.


always_on
---------

If `True`, run in an endless loop. If `False` (default), run in
on/off or on/deep-sleep mode. For on/off, the hardware (via HAL)
has to implement a `shutdown()` method to turn power off.


debug
-----

Print verbose messages while running. Useful for debugging with an
attached console only.


debug_api
---------

Print data passed to and received from the server via the Tesserae
REST-API. Turning this on also only makes sense with an attached
console.


app_name
--------

Blinka/PyGame based systems usually don't have a NVRAM for persisting
the token and etag of the dashboard. `app_config.app_name` will be
used in this case to emulate the NVRAM in
`$HOME/.local/share/Tesserae-<app_name>/nvram.data`.


run_interval
------------

The fallback value for always-on systems between polling the server.


time_table
----------

A defined time-table will force local scheduling, otherwise
scheduling is based on server-side information (`next_poll_s`).

A time-table is a list with one entry for every day starting at Monday.
Every item consists of two tuples:

    (h_start, h_end, h_interval), (m_start, m_end, m_interval)

Start and end are inclusive.

This example will force the display to run Mo-Fr, 9-17 every 15 minutes
regardless of server configuration:

    TT_START   = 0
    TT_INT     = 15
    app_config.time_table = [
      ((9,17,1),(TT_START,59,TT_INT)),
      ((9,17,1),(TT_START,59,TT_INT)),
      ((9,17,1),(TT_START,59,TT_INT)),
      ((9,17,1),(TT_START,59,TT_INT)),
      ((9,17,1),(TT_START,59,TT_INT)),
      (None, None),
      (None, None),
  ]
