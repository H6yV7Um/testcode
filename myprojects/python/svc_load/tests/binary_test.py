import re
from itertools import islice




def b_search(target, seq):
    low = 0
    high = len(seq) - 1
    while low <= high:
        mid = int((low+high)/2)
        guess = seq[mid]
        if target == guess:
            return mid
        if target < guess:
            high = mid -1
        else:
            low = mid + 1

def n_search(target, seq):
    for element in seq:
        if target == element:
            return seq.index(element)

from classic_sort import timer
n = 100000000
target = 99999999
l = list(range(n))
timer(b_search)(target, l)
timer(n_search)(target, l)


