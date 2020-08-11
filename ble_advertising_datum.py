


# ======================================================
# Functions to help with parsing an advertising packet. OLD

def pop_AD(advertising_bytes):
    ad_length = advertising_bytes[0]
    ad_type = advertising_bytes[1]
    ad_bytes = advertising_bytes[2:ad_length + 1]
    ad_rest = advertising_bytes[ad_length + 1:]
    # print("debug: ", ad_type, ad_bytes, ad_rest)
    return ad_type, ad_bytes, ad_rest


ad_names = [None]*256
ad_names[0x01] = "flags"
ad_names[0x02] = "incomplete list of 16-bit Service UUIDs"
ad_names[0x03] = "complete list of 16-bit Service UUIDs"
ad_names[0x04] = "incomplete list of 32-bit Service UUIDs"
ad_names[0x05] = "complete list of 32-bit Service UUIDs"
ad_names[0x06] = "incomplete list of 256-bit Service UUIDs"
ad_names[0x07] = "complete list of 256-bit Service UUIDs"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
ad_names[0x01] = "flags"
def ad_dict_of_se(se):
    ad_names = ["unassigned", "flags", ]
    b = se.advertisement_bytes



def print_advertising_data(advertisement_bytes):
    ab = advertisement_bytes
    while len(ab) > 0:
        ad_type, ad_bytes, ab = pop_AD(ab)
        print_advertising_datum(ad_type, ad_bytes)

def print_advertising_datum(ad_type, ad_bytes):
    print("AD =", ad_type, end='  ')
    for b in ad_bytes:
        print(" {:02x}".format(b), end="")
    print()
    if ad_type == 0x01:
        print("  FLAGS:", end='')
        flags = ad_bytes[0]
        le_flags = flags & 0x03
        bredr_flags = flags - le_flags
        if le_flags == 0:
            print(" Non-discoverable mode, ", end='')
        elif le_flags == 1:
            print(" Limited discoverable mode, ", end='')
        elif le_flags == 2:
            print(" General discoverable mode, ", end='')
        else:
            print(" INVALID DISCOVERABILITY, ", end='')
        if bredr_flags == 0:
            print("no BR/EDR flags")
        else:
            print("<unexpanded BR/EDR flags>")

