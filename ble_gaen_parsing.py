# GAEN parsing
import _bleio

# Each function here takes one _ble scan_entry argument,
# except for same_gaen(se1, se2), which takes two.

# GAEN predicates

def has_gaen_address_type(scan_entry):
    return scan_entry.address.type == _bleio.Address.RANDOM_PRIVATE_NON_RESOLVABLE

def has_gaen_packet_type(scan_entry):
    return not scan_entry.scan_response and not scan_entry.connectable

def starts_with_flags_ad(scan_entry):
    ab = scan_entry.advertisement_bytes
    return len(ab) > 2 and ab[1] == 1

def has_gaen_flags_ad(scan_entry):
    return starts_with_flags_ad(scan_entry) and (scan_entry.advertisement_bytes[2]&2)


def has_gaen_data(scan_entry):
    match = b'\x03\x03\x6F\xFD\x17\x16\x6F\xFD'
    try:
        return scan_entry.advertisement_bytes[-28:].startswith(match)
    except:
        return False

def is_long_gaen(scan_entry):
    return has_gaen_flags_ad(scan_entry) and has_gaen_data(scan_entry)

def is_short_gaen(scan_entry):
    return not starts_with_flags_ad(scan_entry) and has_gaen_data(scan_entry)

def is_gaen(scan_entry):
    return is_short_gaen(scan_entry) or is_long_gaen(scan_entry)

def gaen_recognition_summary(se):
    s = ""
    if is_gaen(se):
        if is_long_gaen(se):
            s = s + "long GAEN packet, "
        else:
            s += "short GAEN packet, "
    else:
        s += "non-GAEN packet, "
    if has_gaen_flags_ad(se):
        s += "GAEN flags, "
    elif starts_with_flags_ad(se):
        s += "flags, "
    if not has_gaen_packet_type(se):
        s += "non-"
    s += "GAEN packet type, "
    if not has_gaen_address_type(se):
        s += "non-"
    s += "GAEN address type"
    return s

# GAEN relationships

def same_gaen(se1, se2):
    same_addr = se1.address == se2.address
    same_bytes = se1.advertisement_bytes == se2.advertisement_bytes
    return same_addr and same_bytes


# GAEN section extraction

def rpi_gaen(scan_entry):
    try:
        return scan_entry.advertisement_bytes[-20:-4]
    except:
        return None

def metadata_gaen(scan_entry):
    try:
        return scan_entry.advertisement_bytes[-4:]
    except:
        return None