# a few functions to help with time


def mm_ss_of_s(s):
    mm, ss = divmod(int(s), 60)
    return "{:02d}:{:02d}".format(mm, ss)

def s_of_ns(ns, ref_ns=0):
    return round( (ns-ref_ns) / 1_000_000_000, 3)
