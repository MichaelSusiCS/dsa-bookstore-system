import numpy as np
import math
from Interfaces import Queue
from Interfaces import Tree


def left(i: int) -> int:
    return 2 * i + 1


def right(i: int) -> int:
    return 2 * i + 2


def parent(i: int) -> int:
    return (i - 1) // 2


def _new_array(n: int) -> np.array:
    return np.zeros(n, object)


class BinaryHeap(Queue, Tree):
    def __init__(self):
        self.a = _new_array(1)
        self.n = 0

    def add(self, x: object):
        if self.n + 1 > len(self.a):
            self._resize()
        self.a[self.n] = x
        self.n += 1
        self._bubble_up_last()
        return True

    def remove(self):
        if self.n == 0:
            return None
        min_val = self.a[0]
        self.n -= 1
        if self.n > 0:
            self.a[0] = self.a[self.n]
            self._trickle_down_root()
        return min_val

    def depth(self, i):
        if i < 0 or i >= self.n:
            return None
        return int(math.floor(math.log2(i + 1)))

    def height(self) -> int:
        if self.n == 0:
            return -1
        return int(math.floor(math.log2(self.n)))

    def bf_order(self) -> list:
        return [self.a[i] for i in range(self.n)]

    def in_order(self) -> list:
        return [self.a[i] for i in self._in_order(0)]

    def post_order(self) -> list:
        return [self.a[i] for i in self._post_order(0)]

    def pre_order(self) -> list:
        return [self.a[i] for i in self._pre_order(0)]

    def size(self) -> int:
        return self.n

    def get_min(self):
        return None if self.n == 0 else self.a[0]

    def _resize(self):
        a = _new_array(max(1, 2 * self.n))
        for i in range(self.n):
            a[i] = self.a[i]
        self.a = a

    def _bubble_up_last(self):
        i = self.n - 1
        while i > 0 and self.a[i] < self.a[parent(i)]:
            p = parent(i)
            self.a[i], self.a[p] = self.a[p], self.a[i]
            i = p

    def _trickle_down_root(self):
        i = 0
        while True:
            l, r = left(i), right(i)
            if l >= self.n:
                break
            smallest = l
            if r < self.n and self.a[r] < self.a[l]:
                smallest = r
            if self.a[i] <= self.a[smallest]:
                break
            self.a[i], self.a[smallest] = self.a[smallest], self.a[i]
            i = smallest

    def _in_order(self, i):
        result = []
        if i < self.n:
            result += self._in_order(left(i))
            result.append(i)
            result += self._in_order(right(i))
        return result

    def _post_order(self, i):
        result = []
        if i < self.n:
            result += self._post_order(left(i))
            result += self._post_order(right(i))
            result.append(i)
        return result

    def _pre_order(self, i):
        result = []
        if i < self.n:
            result.append(i)
            result += self._pre_order(left(i))
            result += self._pre_order(right(i))
        return result

    def __str__(self):
        return str(self.a[0:self.n])
