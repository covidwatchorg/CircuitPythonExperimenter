# A class similar to ScanEntry for _bleio and iterators for it
import time
import _bleio
from ble_gaen_parsing import *
from ble_time import *

class AnnotatedScanEntry():
    def __init__(self, scan_entry, channel=None, s=None):
        if s:
            self.s = s
        else:
            self.s = seconds()
        self.channel = channel
        self._se = scan_entry

    @property
    def address(self):
        return self._se.address

    @property
    def advertisement_bytes(self):
        return self._se.advertisement_bytes

    @property
    def rssi(self):
        return self._se.rssi

    @property
    def connectable(self):
        return self._se.connectable

    @property
    def scan_response(self):
        return self._se.scan_response


def channel_fun(scan_interval, scan_window):
    """returns a function that returns a channel number assuming scanning starts immediately"""
    offset_s = (scan_interval-scan_window)/2  # shifts window to allow for drift
    base_s = seconds() - offset_s
    return (lambda: 37 + int((seconds()-base_s)/scan_interval) % 3)

def annotated_scan( timeout=6.0, interval=0.1, window=0.1, minimum_rssi=-80, filter=(lambda se: True)):
    """returns an iterator for annotated scan entries"""
    scan_interval, scan_window = adjusted_checked_scan_timing(interval, window)
    ch = channel_fun(scan_interval, scan_window)
    scan_entry_iterator = _bleio.adapter.start_scan(
            timeout=timeout,
            interval=scan_interval,
            window=scan_window,
            minimum_rssi=minimum_rssi)
    i = (AnnotatedScanEntry(se, channel=ch()) for se in scan_entry_iterator if filter(se))
    return i

def gse_single(timeout=6.0, minimum_rssi=-75, filter=is_gaen):
    """returns the next annotated GAEN scan_entry"""
    for gse in annotated_scan(timeout=timeout, minimum_rssi=minimum_rssi, filter=filter):
        _bleio.adapter.stop_scan()
        return gse
    return None

def gse_after_gaen_change(start_gse=None, filter=is_gaen):
    """returns the GAEN scan entry shortly after address rotation"""
    if not start_gse:
        start_gse = gse_single(filter=filter)
    if not start_gse:
        return None
    if is_long_gaen(start_gse):
        learned_filter = is_long_gaen
    else:
        learned_filter = is_short_gaen
    minutes = 45
    abort_s = seconds() + 60 * minutes
    while seconds() < abort_s:
        current_gse = gse_single(filter=learned_filter)
        if not current_gse:
            return None
        if not same_gaen(start_gse, current_gse):
            check_gse = gse_single()
            if not check_gse:
                return None
            if same_gaen(current_gse, check_gse):
                return current_gse
    raise Exception( "No change was found after {:d} minutes.".format(minutes))

def gse_burst_list(minimum_rssi=-80, filter=is_gaen):
    """returns a list of channel 37 GAEN packet received in 9 s"""
    return list( annotated_scan(
        timeout=9.5,
        interval=10., window=9.0,
        minimum_rssi=minimum_rssi,
        filter=filter) )


