import numpy as np
from Interfaces import Stack


class ArrayStack(Stack):
    def __init__(self):
        self.n = 0
        self.a = np.zeros(1, dtype=object)  # start with capacity 1

    def resize(self):
        b = np.zeros(max(1, 2 * self.n), dtype=object)
        for i in range(self.n):
            b[i] = self.a[i]
        self.a = b

    def get(self, i: int) -> object:
        if i < 0 or i >= self.n:
            raise IndexError("index out of bounds")
        return self.a[i]

    def set(self, i: int, x: object) -> object:
        if i < 0 or i >= self.n:
            raise IndexError("index out of bounds")
        y = self.a[i]
        self.a[i] = x
        return y

    def add(self, i: int, x: object):
        """
        Insert x at index i (0 <= i <= n), shifting items right.
        """
        if i < 0 or i > self.n:
            raise IndexError("index out of bounds")

        if self.n == len(self.a):
            self.resize()

        # shift right to make space
        for j in range(self.n, i, -1):
            self.a[j] = self.a[j - 1]

        self.a[i] = x
        self.n += 1
        return True

    def remove(self, i: int) -> object:
        """
        Remove and return element at index i (0 <= i < n), shifting left.
        """
        if i < 0 or i >= self.n:
            raise IndexError("index out of bounds")

        x = self.a[i]

        # shift left to fill the gap
        for j in range(i, self.n - 1):
            self.a[j] = self.a[j + 1]

        self.n -= 1

        # shrink if too empty (never below capacity 1)
        if len(self.a) >= 3 * self.n and len(self.a) > 1:
            self.resize()

        return x

    def push(self, x: object):
        # push to top
        return self.add(self.n, x)

    def pop(self) -> object:
        if self.n == 0:
            raise IndexError("pop from empty stack")
        return self.remove(self.n - 1)

    def size(self):
        return self.n

    def __str__(self):
        s = "["
        for i in range(self.n):
            s += "%r" % self.a[i]
            if i < self.n - 1:
                s += ","
        return s + "]"

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < self.n:
            x = self.a[self.iterator]
            self.iterator += 1
            return x
        raise StopIteration()

    def __contains__(self, item):
        return item in self.a
