# some GAEN measurments

import gc
import time
import _bleio
import ble_print
from ble_print import print_scan_entry, hex_of_bytes
import ble_gaen_parsing
from ble_gaen_parsing import is_gaen, gaen_recognition_summary, same_gaen
from ble_gaen_parsing import rpi_gaen, metadata_gaen

def mm_ss_of_s(s):
    mm, ss = divmod(int(s), 60)
    return "{:02d}:{:02d}".format(mm, ss)

def s_of_ns(ns, ref_ns=0):
    return round( (ns-ref_ns) / 1_000_000_000, 3)

def stats_of_number_list( nums ):
    n = len(nums)
    if n == 0:
        raise Exception( "Cannot print stats of an empty number list")
    numbers = nums[:]  # copy
    numbers.sort()
    total = sum(numbers)
    ave = total / n
    top = max(numbers)
    bottom = min(numbers)
    middle = numbers[int(n/2)]
    f = "n = {:d},  sum = {:2.3f},  mean = {:1.3f},  max = {:1.3f},  min = {:1.3f},  median = {:1.3f}"
    return f.format(n, total, ave, top, bottom, middle)

# ======== Find a BLE Radio and low-level interface ========
ble = _bleio.adapter
ble.erase_bonding()
# ==========================================================

# ==========================================================
# nschse
# Some acquisition functions return tuples of
#      the monotonic ns register
#      the channel number
#      the ScanEntry (scan_entry)
# from a scan, called nschse. The ns is close to
# the relative time that the Scanentry was created. An inherited
# class might not work because of the nature of a ScanEntry.

# Return the scan_entry for the next packet *noticed*
# (exception if not found in timeout seconds)
def single_nschse(timeout=6.0, minimum_rssi=-75, channel=None, filter=None):
    if not filter:
        filter = lambda se : True
    t0 = time.monotonic_ns
    interval = 0.175
    window = interval / 2.0 + .002
    t_offset = -(interval - window) / 2.0 * 1_000_000_000
    t0 = t_offset + time.monotonic_ns()
    for scan_entry in ble.start_scan(
            timeout=timeout,
            interval=interval,
            window=window,
            minimum_rssi=minimum_rssi):
        t = time.monotonic_ns()
        probable_channel = ( int((t-t0)/interval) % 3 ) + 37
        if ( not channel or channel == probable_channel ) and filter(scan_entry):
            ble.stop_scan()
            return (t, probable_channel, scan_entry)
    raise Exception("no specified packet in {:3f} seconds".format(timeout))

# get nschse until the gaen packet changes and then return the one afte that
def nschse_after_GAEN_change(start_nschse=None):
    if not start_nschse:
        start_nschse = single_nschse(filter=is_gaen)
    current_ns, ch, start_se = start_nschse
    abort_ns = current_ns + 60 * 60_000_000_000 # hour later
    while time.monotonic_ns() < abort_ns:
        ns, ch, current_se = single_nschse(filter=is_gaen)
        if not same_gaen(start_se, current_se):
            ns_alt, ch, check_se = single_nschse()
            if same_gaen(current_se, check_se):
                break
    return ns, ch, current_se


# ============ some canned measurements and reports =========

def print_time_between_address_changes(n=1):
    print("Time between GAEN advertisement address changes")
    columns = "{:^8}   {:^30}   {:^49}   {:^11}"
    print(columns.format("duration", "address", "RPI", "AEM"))
    nschse_prev = nschse_after_GAEN_change()
    for _ in range(n):
        tp, chp, sep = nschse_prev
        nschse = nschse_after_GAEN_change(nschse_prev)
        t, ch, se = nschse
        duration = mm_ss_of_s( s_of_ns(t, tp) )
        address = str(se.address)
        rpi = hex_of_bytes(rpi_gaen(se))
        aem = hex_of_bytes(metadata_gaen(se))
        print( columns.format(duration, address, rpi, aem) )
        nschse_prev = nschse


# print a few packets (try is_gaen for filter)
def print_a_few_packets(number_of_packets=20, channel=None, filter=None):
    print("---------  Details for {:2d} packets  --------".format(number_of_packets))
    t0 = time.monotonic_ns()
    for count in range(number_of_packets):
        ns, channel, scan_entry = single_nschse(channel=None, filter=is_gaen)
        print("#", count, "    ", s_of_ns(ns, t0), "s since start     channel =",
            channel, "  rssi =", scan_entry.rssi, end="    ")
        print_scan_entry(scan_entry)
        print(gaen_recognition_summary(scan_entry))
        print("----------------------------------------------")
    print()

# The nschse from consequtive scanned advertisement packets
# in 7-9 s time.
def nschse_list(minimum_rssi=-80):
    return [ (time.monotonic_ns(), 37, se)
               for se
               in ble.start_scan(timeout=9.5, interval=10., window=9.0, minimum_rssi=minimum_rssi)
               if is_gaen(se)]

def print_advertising_interval_stats(minimum_rssi=-80):
    print("advertising interval measurement stats of intervals 180 ms to 330 ms over 36 s")
    print("NB: Make sure only one phone is nearby.")
    ns_list = [ ns for ns, ch, se in nschse_list(minimum_rssi=minimum_rssi) ]
    if len(ns_list) < 7:
        raise Exception("Not enough packets")
    intervals = [s_of_ns(a - b) for a, b in zip(ns_list[1:], ns_list[:-1])]
    intervals = [i for i in intervals if i > 0.180 and i < 0.330]
    print( stats_of_number_list(intervals) )
    print()


# =================================
# Testing
# =================================


# _bleio scanning example: counting packets in one second
count = 0
for scan_entry in ble.start_scan(timeout=1.0):
    count += 1
print("number of packets found in one second:", count)

# printing packets with filtering
print_a_few_packets(number_of_packets=5, filter=is_gaen)

# Measuring advertising interval
print_advertising_interval_stats()

# Measuring time between RPI changes
print_time_between_address_changes(n=5)

