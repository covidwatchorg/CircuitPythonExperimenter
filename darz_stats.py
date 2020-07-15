# a few helper functions related to statistics


def stats_of_number_list( nums ):
    """Returns a string describing the number list."""
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