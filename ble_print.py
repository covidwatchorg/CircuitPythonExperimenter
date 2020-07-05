# printing advertising packets and support formatting
import _bleio

# ======================================================
# Functions to help with printing a generic advertising packet.

def hex_of_bytes(bb):
    s = ""
    count = 0
    for b in bb:
        s += (" {:02x}".format(b))
        count += 1
        if count % 8 == 0:
            s += " "
    return s.strip()

def print_scan_entry_type(scan_entry):
    if scan_entry.scan_response:
        print("Scan Response", end='')
    else:
        print("Advertisement", end='')
    if scan_entry.connectable:
        print(", connectable")
    else:
        print("")


def print_address(address):
    print("address =", address, end="  ")
    t = address.type
    print("address type =", end=" ")
    if t == address.PUBLIC:
        print("PUBLIC")
    elif t == address.RANDOM_STATIC:
        print("RANDOM_STATIC")
    elif t == address.RANDOM_PRIVATE_RESOLVABLE:
        print("RANDOM_PRIVATE_RESOLVABLE")
    elif t == address.RANDOM_PRIVATE_NON_RESOLVABLE:
        print("RANDOM_PRIVATE_NON_RESOLVABLE")
    else:
        print("unknown")


def print_advertisement_bytes(scan_entry):
    adv_bytes = bytearray(scan_entry.advertisement_bytes)
    if len(adv_bytes) != 0:
        print("advertisement bytes = ", hex_of_bytes(adv_bytes))


def print_scan_entry(scan_entry):
    print_scan_entry_type(scan_entry)
    print_address(scan_entry.address)
    print_advertisement_bytes(scan_entry)
