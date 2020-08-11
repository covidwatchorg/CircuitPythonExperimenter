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


# ============ some canned measurements and reports =========

def print_time_between_address_changes(n=1):
    print("Time between GAEN advertisement address changes")
    columns = "{:^8}   {:^30}   {:^49}   {:^11}"
    print(columns.format("duration", "address", "RPI", "AEM"))
    gse_prev = gse_after_gaen_change()
    for _ in range(n):
        gse = gse_after_gaen_change(gse_prev)
        duration = mm_ss_of_s( gse.s - gse_prev.s )
        address = str(gse.address)
        rpi = hex_of_bytes(rpi_gaen(gse))
        aem = hex_of_bytes(metadata_gaen(gse))
        print( columns.format(duration, address, rpi, aem) )
        gse_prev = gse


# print a few packets (try is_gaen for filter)
def print_a_few_packets(number_of_packets=20, channel=None, filter=lambda se: True):
    print("---------  Details for {:2d} packets  --------".format(number_of_packets))
    print("...collecting packets...")
    ble.stop_scan()
    list_of_index_gse = [pair
                         for pair
                         in zip(range(number_of_packets), annotated_scan(filter=filter))]
    ble.stop_scan()
    for index, gse in list_of_index_gse:
        print("#", index, "    ", gse.s, "s   channel =", gse.channel, "  rssi =", gse.rssi, end="    ")
        print_scan_entry(gse)
        print(gaen_recognition_summary_string(gse))
        print("----------------------------------------------")
    print()


def print_advertising_interval_stats(minimum_rssi=-80):
    print("advertising interval measurement stats")
    print("NB: Make sure only one phone is nearby.")
    ble.stop_scan()
    s_list = [ gse.s for gse in gse_burst_list(minimum_rssi=minimum_rssi) ]
    ble.stop_scan()
    if len(s_list) < 7:
        raise Exception("There are insuficient packets to study the advertising interval.")
    intervals = [(a - b) for a, b in zip(s_list[1:], s_list[:-1])]
    print("All:       ", stat_string_of_number_list(intervals) )
    intervals = [i for i in intervals if i > 0.180 and i < 0.330]
    print("180-330 ms:", stat_string_of_number_list(intervals) )
    print()


# =================================
# Testing
# =================================

gc.collect()
reset_seconds()

# printing packets with filtering
print_a_few_packets(number_of_packets=120, filter=is_gaen)

# Measuring advertising interval
print_advertising_interval_stats()

# Measuring time between RPI changes
print_time_between_address_changes(n=50)

