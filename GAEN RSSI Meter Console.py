# GAEN RSSI Meter
# Console version

import gc
import time
import math
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

# Uncomment only the line that selects the filter you want.
# filter = ["EN packets are collected from any phone.", is_gaen"]
filter = ["EN packets are collected from any iPhone", is_long_gaen]   # Apple
# filter = ["EN packets are collected from any Android phone.", is_short_gaen]  # Google
# filter = ["All packets are collected from any device.", lambda gse: True]

# Length of the measurement shutter-open in seconds
burst_s = 4.0   # 0.1 to 9.5 (for ch37) or ...

# Whether sampling is from channel 37 only
ch37 = True

# what channels to consider
# channels = [37]
#channels = [37, 38, 39]

# Start of burst to start of burst in seconds
bb_s = 10.0

# Advertising timing to use when ch37 is False
scan_window = 0.30  # Perhaps 0.03 for iOS
scan_interval = 0.40  # Perhaps 0.04 for iOS

if bb_s < burst_s > bb_s or (ch37 and burst_s > 10.):
    raise Exception("The the shutter time is too long for the rest of the parameters.")

t = """A measurement is made each 'frame'.
A measurement consists of aggregations over the the "shutter" time:
     Count
     Mean
     Max
Each measurement is logged. 
The frame length is about 4 minutes for GAEN phones,
but are typically a lot shorter (5 s) for testing.
The shutter time is typically 4 s.
Sampling can be made from only channel 37 or from all channels.
If sampling is limited to channel 37,
the shutter time is capped at 9.5 s and the scan window is longer.
If all channels are sampled,
then the scan window and scan interval may be set. 
You can set whether an iPhone, an Android phones or either is logged.
Only one should be in the vicinity. 
The bar starts at -80 dB and shows mean as 'x', overlaying max as ']'. """

print()
print("==============================================")
print(t)
print("==============================================")
print()

print("Shutter time (sampling period): ", burst_s)
print("Time between start of measurement frames: ", bb_s)
if ch37:
    print("Channels: 37")
    print("Duty cycle: 1.0")
else:
    print("Channels: 37, 38, 39")
    print("Duty cycle: {:0.2f}".format(scan_window/scan_interval))
    print("Scan Window:", scan_window)
    print("Scan Interval:", scan_interval)
print(filter[0])
print()

if ch37:
    interval = 10.1
    window = 10.05
else:
    interval = scan_interval
    window = scan_window

gc.collect()
reset_seconds_needed = True

print("                            -80dB")
print("         packet  RSSI   RSSI  |")
print("seconds  count   mean   max   |")
frame_count = 0
mean_sum = 0.
max_sum = 0
n_sum = 0

while True:
    for row in range(10):
        if reset_seconds_needed:
            reset_seconds_needed = False
            reset_seconds()
        start_s = seconds()
        scn_i = annotated_scan(timeout=burst_s, interval=interval, window=window, filter=filter[1])
        rssi_list = [gse.rssi for gse in scn_i]
        # s = seconds()
        ble.stop_scan()
        n = len(rssi_list)
        if n == 0:
            f = "{:6.1f}   {:3d}    -----   ---   |"
            print(f.format(start_s, n))
        else:
            ave = sum(rssi_list) / n
            top = max(rssi_list)
            meter = 'x' * round(max(0,ave+80.)) + ']' * round(top-ave)
            f = "{:6.1f}   {:3d}    {:3.1f}   {:3.0f}   |"
            print(f.format(start_s, n, ave, top) + meter)
            frame_count += 1
            mean_sum += ave
            max_sum += top
            n_sum += n
        ble.enabled = False
        gc.collect()
        if row == 9:
            f = "average:  {:3.1f}  {:3.1f}   {:3.1f} |"
            k = frame_count
            if k > 0:
                print(f.format(n_sum/k, mean_sum/k, max_sum/k))
            print("------------------------------|")
            print("seconds  count   mean   max   |")
            frame_count = 0
            mean_sum = 0.
            max_sum = 0
            n_sum = 0
        ble.enabled = True
        while seconds() < start_s + bb_s:
            pass


