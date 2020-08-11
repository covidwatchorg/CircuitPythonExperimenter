# some GAEN measurments

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

# Uncomment the applicable line
# filter = is_gaen        # first of Apple or Google source seen
filter = is_long_gaen   # Apple only
#filter = is_short_gaen  # Google only

# Edit to set the maximum length of time for measurements
timeout_hh_mm = "05:30"

# ============ some canned measurements and reports =========

def print_time_between_address_changes(timeout_hh_mm="0:50", filter=is_gaen):
    columns = "{:^8}     {:^30}   {:^49}   {:^11}"
    hh, mm = timeout_hh_mm.split(':')
    abort_seconds = 60 * (60*int(hh)+float(mm)) + seconds()
    seed = None
    gse_prev = None
    while seconds() < abort_seconds:
        if not seed:
            seed = gse_single(timeout=10.0, minimum_rssi=-70, filter=filter)
            if not seed:
                print("Aborting, no packets are found")
                return None
            if is_long_gaen(seed):
                print("Time between Apple EN advertisement address rotations")
            else:
                print("Time between Google EN advertisement address rotations")
            print(columns.format("duration", "address", "RPI", "AEM"))
            gse_prev = gse_after_gaen_change(seed)
            if not gse_prev:
                print("Aborting, no initial change in address is found")
                return None
        gse = gse_after_gaen_change(gse_prev)
        if gse:
            duration = mm_ss_of_s(gse.s - gse_prev.s)
            address = str(gse.address)
            rpi = hex_of_bytes(rpi_gaen(gse))
            aem = hex_of_bytes(metadata_gaen(gse))
            print( columns.format(duration, address, rpi, aem) )
            gse_prev = gse
        else:
            print("Lost advertiser, waiting a minute, then restarting")
            time.sleep(60)
            seed = None
        gc.collect()



# =================================
# Testing
# =================================

gc.collect()
reset_seconds()
print("GAEN Address Rotation Timer")
# Measuring time between RPI changes
print_time_between_address_changes(timeout_hh_mm=timeout_hh_mm, filter=filter)

