#!/bin/bash
# --------------------------------------------------------------------------
# This script installs files and services for a Tesserae-Client running as
# an appliance on a Raspberry Pi.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# --------------------------------------------------------------------------

PROJECT="tesserae-device-circuitpython"
CONFIG="/etc/$PROJECT"
SYS_USER="tesserae_client"
SYS_USER_HOME="/usr/local/lib/$SYS_USER"

# --- create system-user   --------------------------------------------------

create_sys_user() {
  if ! grep -q "$SYS_USER" /etc/passwd; then
    echo -e "[INFO] create system-user $SYS_USER:$SYS_USER" 2>&1
    groupadd -r $SYS_USER
    adduser --gecos "" --system --group \
                              --home "$SYS_USER_HOME" $SYS_USER
    usermod -a -G render,video $SYS_USER
  fi
}

# --- install packages   ---------------------------------------------------

install_packages() {
  echo -e "[INFO] installing system-packages" 2>&1
  # system packages
  apt-get -y update
  apt-get -y install rsync swig python3-dev
  apt-get -y install python3-pygame python3-rpi.gpio libsdl2-2.0 \
                          libegl1 libgl1 libgl1-mesa-dri

  # python packages: install into virtual environment
  echo -e "[INFO] installing virtual environment" 2>&1
  python3 -m venv --system-site-packages "$SYS_USER_HOME/venv.tesserae"
  . "$SYS_USER_HOME/venv.tesserae/bin/activate"
  pip install blinka-displayio-pygamedisplay
  pip install adafruit-circuitpython-display-text
  chown -R "$SYS_USER:$SYS_USER" "$SYS_USER_HOME"
}

# --- install specific files   ----------------------------------------------

install_files() {
  echo -e "[INFO] installing project files" 2>&1

  rand="$RANDOM"
  if [ -d "$CONFIG" ]; then
    # save current configuration
    mv "$CONFIG" "$CONFIG.$rand"
  fi

  # install standard files
  for f in `find $(dirname "$0")/../files/ -type f -not -name "*.pyc"`; do
    target="${f#*files}"
    target_dir="${target%/*}"
    [ ! -d "$target_dir" ] && mkdir -p "$target_dir"
    cp "$f" "$target"
    chown root:root "$target"
  done

  chmod 755 "$CONFIG"
  chmod 644 "$CONFIG/env.sh"
  chmod 644 "/etc/systemd/system/$PROJECT.service"
  chmod 644 "/usr/local/bin/$PROJECT.service"

  # restore old configuration
  if [ -f "$CONFIG.$rand" ]; then
    mv -f "$CONFIG" "$CONFIG.new"
    mv "$CONFIG.$rand" "$CONFIG"
    echo -e "[INFO] new version of configuration files saved to: $CONFIG.new" 2>&1
  fi
}

# --- install client   ------------------------------------------------------

install_client() {
  echo -e "[INFO] installing client to $SYS_USER_HOME/$PROJECT" 2>&1
  cd $(dirname "$0")/../..
  rsync -av --delete --exclude=src/settings.py \
                     --exclude=.git \
                     --exclude=__pycache__ \
                     "$PROJECT" "$SYS_USER_HOME"
  chown -R "$SYS_USER:$SYS_USER" "$SYS_USER_HOME/$PROJECT"

  if [ ! -f "$CONFIG/settings.py" ]; then
    echo -e "[INFO] creating $CONFIG/settings.py" 2>&1
    cp \
      "$SYS_USER_HOME/$PROJECT/src/settings_template.py" \
         "$CONFIG/settings.py"
    ln -s "$CONFIG/settings.py" \
               "$SYS_USER_HOME/$PROJECT/src/settings.py"
  fi
}

# --- activate service   ----------------------------------------------------

enable_services() {
  echo -e "[INFO] enabeling $PROJECT.service" 2>&1
  systemctl enable "$PROJECT.service"
}

# --- main program   --------------------------------------------------------

create_sys_user
install_packages
install_files
install_client
enable_services

echo "Please edit $CONFIG/env.sh and $CONFIG/settings.py"
echo "and run \"sudo systemctl start $PROJECT.service\" to activate changes"
