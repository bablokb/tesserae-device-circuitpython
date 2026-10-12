# ----------------------------------------------------------------------------
# Message translations for es.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import status

MSG_TABLE = {
  status.WAITING     : "Esperando registro por el administrador",
  status.NO_PUSH     : "Aún no hay ningún panel disponible",
  status.ERR_MAC     : "Dirección MAC duplicada, se requiere intervención",
  status.ERR_NET     : "Error de red (puede ser temporal)",
  status.ERR_UNKNOWN : "Error desconocido",
  }
