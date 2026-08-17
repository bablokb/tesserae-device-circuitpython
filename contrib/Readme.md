Example Hardware Configurations
===============================

This directory contains a number of examples for possible hardware
configuration files.

Most of them can't be used as is, since at least the specific pin
configuration needs some tweaking. Instead of editing these files in
place, copy them to `src/local` and edit them there.

For devboards with builtin hardware, it makes more sense to create a
hardware abstraction layer file instead. These files are distributed
with the
[base-application](https://github.com/bablokb/circuitpython-base-app)
and can be reused across different applications.
