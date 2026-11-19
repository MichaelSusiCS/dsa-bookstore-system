import numpy as np
from Interfaces import Queue


class ArrayQueue(Queue):
    def __init__(self):
        self.n = 0          # number of elements
        self.j = 0          # index of head
        self.a = np.zeros(1, dtype=object)  # start with capacity 1

    def resize(self):
        """
        creates a new array that maintains the
        array size invariant and copies the old values
        in FIFO order
        """
        b = np.zeros(max(1, 2 * self.n), dtype=object)
        old_len = len(self.a)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % old_len]
        self.a = b
        self.j = 0

    def add(self, x: object):
        """
        adds element x to the tail of the queue
        """
        if self.n == len(self.a):
            self.resize()

        self.a[(self.j + self.n) % len(self.a)] = x
        self.n += 1
        return True

    def remove(self) -> object:
        """
        removes and returns the element at the head
        """
        if self.n == 0:
            raise IndexError("remove from empty queue")

        x = self.a[self.j]
        self.j = (self.j + 1) % len(self.a)
        self.n -= 1

        # shrink if array is too empty (but never below capacity 1)
        if len(self.a) >= 3 * self.n and len(self.a) > 1:
            self.resize()

        return x

    def size(self):
        return self.n

    def __str__(self):
        s = "["
        for i in range(self.n):
            s += "%r" % self.a[(self.j + i) % len(self.a)]
            if i < self.n - 1:
                s += ","
        return s + "]"

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < self.n:
            x = self.a[(self.j + self.iterator) % len(self.a)]
            self.iterator += 1
            return x
        raise StopIteration()
