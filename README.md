# CircuitPythonExperimenter

A collection of CircuitPython code for Bluetooth LE sniffing in service of Contact Tracing development

This repo is initially a collection of CircuitPython code, contributed by Dar Scott, which he has been using for sniffing Bluetooth LE packets using CircuitPython installed on an Adafruit nRF board. 

It includes a crypto file from James Petrie that uses cryptography.hazmat functions.. 

This description assumes a fundamental knowledge of using CircuitPython.

The .py files with all lower-case and no spaces are library files. Drop them into Volumes/CIRCUITPY/lib.

The files that start with "GAEN" and include spaces little programs that each perform one function. Take one, edit it as needed, and save it as main.py in Volumes/CIRCUITPY. Any other .py at the root of that drive should be removed. 

The "little programs" often have parameters near the top of the .py files that can be varied to vary the functionality. 

Some "little programs":

**GAEN Address Rotation Timer**
**GAEN Advertising Interval Timer**
**GAEN RSSI Meter Console** The text version of the RSSI meter.
**GAEN Advertising Source** Very incomplete.
**GAEN Sniffer** Old, maybe the name can be reused.

Perhaps coming are a GAEN implementation, and some GAEN advertisers. Perhaps some proposed metheds can be prototyped here. 

Sharing and contributions encouraged.
