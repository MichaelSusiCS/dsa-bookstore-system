import random
from Interfaces import List


def linear_search(a: List, x: object):
    """
    uses the linear search algorithm to return the index of the given
    element if it is found in the given list; otherwise returns None.
    """
    for i in range(a.size()):
        if a.get(i) == x:
            return i
    return None


def binary_search(a: List, x: object):
    """
    uses the binary search algorithm to return the index of the given
    element if it is found in the given SORTED list; otherwise returns None.
    """
    low = 0
    high = a.size() - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = a.get(mid)

        if mid_val == x:
            return mid
        elif mid_val < x:
            low = mid + 1
        else:
            high = mid - 1

    return None


def _merge(a0: List, a1: List, a: List):
    """
    merges sorted lists a0 and a1 into sorted list a
    """
    i = j = k = 0

    while i < a0.size() and j < a1.size():
        if a0.get(i) <= a1.get(j):
            a.set(k, a0.get(i))
            i += 1
        else:
            a.set(k, a1.get(j))
            j += 1
        k += 1

    while i < a0.size():
        a.set(k, a0.get(i))
        i += 1
        k += 1

    while j < a1.size():
        a.set(k, a1.get(j))
        j += 1
        k += 1


def merge_sort(a: List):
    """
    sorts the given list using the merge sort algorithm
    """
    if a.size() <= 1:
        return

    mid = a.size() // 2
    left = a.__class__()
    right = a.__class__()

    for i in range(mid):
        left.append(a.get(i))
    for i in range(mid, a.size()):
        right.append(a.get(i))

    merge_sort(left)
    merge_sort(right)
    _merge(left, right, a)


def _partition_f(a: List, start: int, end: int):
    """
    partition using first element as pivot
    """
    pivot = a.get(start)
    i = start + 1

    for j in range(start + 1, end + 1):
        if a.get(j) <= pivot:
            temp = a.get(i)
            a.set(i, a.get(j))
            a.set(j, temp)
            i += 1

    temp = a.get(start)
    a.set(start, a.get(i - 1))
    a.set(i - 1, temp)

    return i - 1


def _partition_r(a: List, start: int, end: int):
    """
    partition using random element as pivot
    """
    r = random.randint(start, end)
    temp = a.get(start)
    a.set(start, a.get(r))
    a.set(r, temp)
    return _partition_f(a, start, end)


def _quick_sort_f(a: List, start: int, end: int):
    if start >= end:
        return

    p = _partition_f(a, start, end)
    _quick_sort_f(a, start, p - 1)
    _quick_sort_f(a, p + 1, end)


def _quick_sort_r(a: List, start: int, end: int):
    if start >= end:
        return

    p = _partition_r(a, start, end)
    _quick_sort_r(a, start, p - 1)
    _quick_sort_r(a, p + 1, end)


def quick_sort(a: List, p=True):
    """
    sorts the given List using the quick sort algorithm.
    """
    if a.size() <= 1:
        return

    if p:
        _quick_sort_r(a, 0, a.size() - 1)
    else:
        _quick_sort_f(a, 0, a.size() - 1)
