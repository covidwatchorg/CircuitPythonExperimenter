# a few stats helpers

def stat_string_of_number_list(nums):
    """returns a summary string for a list of numbers"""
    f = "count = {:d},  sum = {:2.3f}"
    n = len(nums)
    numbers = nums[:]  # copy
    numbers.sort()
    total = sum(numbers)
    s = f.format(n, total)
    if n > 1:
        ave = total / n
        top = numbers[-1]
        bottom = numbers[0]
        middle = numbers[int(n / 2)]
        f = ",   ave = {:1.3f},  max = {:1.3f},  min = {:1.3f},  median = {:1.3f}"
        s += f.format(ave, top, bottom, middle)
    return s

# def histogram_of_number_list(nums, start_val=None, end_val=None, n_bins, bin_size=None):
#     n_bins = len(nums)/5 + 1
#     if not start_val:
#         start_val = min(nums)
#     if not end_val:
#         end_val = max(nums)
#     span = end_val - start_val
#     if not bin_size:
#         n_bins = len(nums)/5 + 1
#         bin_size = span/n_bins
#     else:
#         n_bins = int(span/bin_size) + 1
#     # adjust
#
#
#     return start_val, step_val, count_list