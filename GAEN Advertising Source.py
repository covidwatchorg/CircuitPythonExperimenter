# GAEN Advertising Source

import gc
import time
import _bleio
from ble_time import *
from darz_stats import *
from ble_print import *
from ble_gaen_parsing import *
from ble_gaen_scanning import *

reset_seconds()

# ======== Find a BLE Radio and low-level interface ========
ble = _bleio.adapter
ble.erase_bonding()
# ==========================================================

