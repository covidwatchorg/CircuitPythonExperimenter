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



def print_advertising_interval_stats(minimum_rssi=-80, filter=is_short_gaen, family="Unknown"):
    ble.stop_scan()
    s_list = [ gse.s for gse in gse_burst_list(minimum_rssi=minimum_rssi, filter=filter) ]
    ble.stop_scan()
    if s_list and len(s_list) > 6:
        print("-------- ", family, "--------")
        intervals = [(a - b) for a, b in zip(s_list[1:], s_list[:-1])]
        print("All:       ", stat_string_of_number_list(intervals))
        intervals = [i for i in intervals if 0.200 < i < 0.330]
        print("200-330 ms:", stat_string_of_number_list(intervals) )
        # ai = median(intervals)*1000.0 - 5.0
        # print("Advertising Interval: ", ai, " ms")
        print()


# =================================
# Testing
# =================================

gc.collect()
reset_seconds()

print("GAEN Advertising Interval Timing")
print()
print("NB: Make sure you have at least one phone nearby,")
print("    but no more than one iPhone,")
print("    and no more than one Android phone.")
print()

# Measuring advertising interval
print_advertising_interval_stats(filter=is_long_gaen, family="Apple")
print_advertising_interval_stats(filter=is_short_gaen, family="Google")

