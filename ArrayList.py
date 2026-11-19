import numpy as np
from Interfaces import List


class ArrayList(List):
    """
    ArrayList: Implementation of a List interface using Arrays.
    """

    def __init__(self, a: list = None):
        """
        constructor creates an ArrayList object, empty or filled from list a
        """
        self.j = 0
        if a is None:
            self.n = 0
            self.a = np.zeros(self.n, object)
        else:
            self.n = len(a)
            self.a = np.zeros(max(1, self.n), object)
            for i in range(self.n):
                self.a[i] = a[i]

    def resize(self):
        """
        helper method; creates a new array that maintains the
        array size invariant and copies the old values.
        """
        # new capacity: max(1, 2n)
        b = np.zeros(max(1, 2 * self.n), object)

        # copy elements in logical order: b[k] = a[(j+k) mod len(a)]
        # (only run if there are elements; also avoids mod-by-zero when len(a)==0)
        old_len = len(self.a)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % old_len]

        self.a = b
        self.j = 0

    def get(self, i: int) -> object:
        """
        returns the element at position i
        """
        if i < 0 or i >= self.n:
            raise IndexError()
        return self.a[(self.j + i) % len(self.a)]

    def set(self, i: int, x: object) -> object:
        """
        sets the value at index i to be x and returns the old value
        """
        if i < 0 or i >= self.n:
            raise IndexError()
        idx = (self.j + i) % len(self.a)
        y = self.a[idx]
        self.a[idx] = x
        return y

    def append(self, x: object):
        """
        adds a new element to the end of this list
        :param x: Object type; the new element to add
        :return: None
        """
        self.add(self.n, x)

    def add(self, i: int, x: object):
        """
        inserts x at index i by shifting left or right depending on half
        """
        if i < 0 or i > self.n:
            raise IndexError()

        # handle starter capacity = 0
        if len(self.a) == 0:
            self.a = np.zeros(1, object)
            self.j = 0

        if self.n == len(self.a):
            self.resize()

        m = len(self.a)

        if i < self.n / 2:
            # shift left side left by moving j backward
            for k in range(0, i):
                self.a[(self.j + k - 1) % m] = self.a[(self.j + k) % m]
            self.j = (self.j - 1) % m
        else:
            # shift right side right
            for k in range(self.n - 1, i - 1, -1):
                self.a[(self.j + k + 1) % m] = self.a[(self.j + k) % m]

        self.a[(self.j + i) % m] = x
        self.n += 1

    def remove(self, i: int) -> object:
        """
        removes and returns element at index i
        """
        if i < 0 or i >= self.n:
            raise IndexError()

        m = len(self.a)
        x = self.a[(self.j + i) % m]

        if i < self.n / 2:
            # shift left half right
            for k in range(i, 0, -1):
                self.a[(self.j + k) % m] = self.a[(self.j + k - 1) % m]
            self.j = (self.j + 1) % m
        else:
            # shift right half left
            for k in range(i, self.n - 1):
                self.a[(self.j + k) % m] = self.a[(self.j + k + 1) % m]

        self.n -= 1

        # keep array-size invariant (shrink when too empty)
        if self.n == 0:
            # optional: keep capacity at 1 so add() never fights len==0
            self.a = np.zeros(1, object)
            self.j = 0
        elif len(self.a) >= 3 * self.n:
            self.resize()

        return x
   
    def size(self) -> int:
        """
        returns the size of this list
        :return: int type; the number of elements in this list
        """
        return self.n

    def index_of(self, x):
        """
        returns the list index of element x if exists in the list
        or None, otherwise.
        :param x: object type;
        :return: int type; the index of x in the list; None if x is not in the list
        """
        for i in range(self.a):
            if self.a[i] == x:
                return i
        return None

    def __str__(self):
        s = "["
        for i in range(0, self.n):
            s += "%r" % self.a[(i + self.j) % len(self.a)]
            if i < self.n - 1:
                s += ","
        return s + "]"

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < self.n:
            x = self.a[(self.iterator + self.j) % len(self.a)]
            self.iterator += 1
        else:
            raise StopIteration()
        return x

    def __getitem__(self, key):
      if isinstance(key, int):
          # Single index
          if key < 0 or key >= self.n:
              raise IndexError("Index out of range")
          return self.get(key)
      elif isinstance(key, slice):
          # Slice
          start, stop, step = key.indices(self.n)
          result = ArrayList()
          for i in range(start, stop, step):
              result.append(self.get(i))
          return result
      else:
          raise TypeError("Invalid argument type")
