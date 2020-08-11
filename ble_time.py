# Some functions to help with timing and BLE timing in particular
import time


_ns_offset = 0

def core_ns():
    return time.monotonic_ns()

def reset_seconds():
    global _ns_offset
    _ns_offset = core_ns()

def seconds():
    global _ns_offset
    return (core_ns() - _ns_offset) * 0.000_000_001


def delta_t_fun():
    """returns a function that returns the seconds since that function was created"""
    base = seconds()
    return lambda: seconds() - base

# BLE intervals and windows

def ble_time_round(t):
    return 0.000625 * round(t/0.000625)

# non-con
def check_advertising_interval(t):
    if t<0.1 or t>10.24:
        raise Exception( "The advertising interval {:d} is NOT in the allowed range.".format(t))

def check_scan_interval(t):
    if t<0.01 or t>10.24:
        raise Exception( "The scan interval {:d} s is NOT in the allowed range.".format(t))

def check_scan_window(t, scan_interval=10.24):
    if t<0.01 or t>scan_interval:
        raise Exception( "The scan window {:d} s is NOT in the allowed range.".format(t))

def adjusted_checked_scan_timing(interval, window):
    """returns a new (scan_interval, scan_window) after adjusting and checking"""
    scan_interval = ble_time_round(interval)
    scan_window = ble_time_round(window)
    check_scan_window(scan_window)
    check_scan_window(scan_window, scan_interval)
    return (scan_interval, scan_window)

# report support

def mm_ss_of_s(s):
    mm, ss = divmod(int(s), 60)
    return "{:02d}:{:02d}".format(mm, ss)

def s_of_ns(ns, ref_ns=0):
    return round( (ns-ref_ns) / 1_000_000_000, 3)
