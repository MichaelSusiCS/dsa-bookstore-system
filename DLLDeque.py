from Interfaces import Deque
from DLList import DLList


class DLLDeque(Deque, DLList):
    def __init__(self):
        DLList.__init__(self)

    def add_first(self, x: object):
        self.add(0, x)

    def add_last(self, x: object):
        self.add(self.n, x)

    def remove_first(self) -> object:
        return self.remove(0)

    def remove_last(self) -> object:
        return self.remove(self.n - 1)

    def clear(self):
        # Reset to empty state (sentinel points to itself)
        self.dummy.next = self.dummy
        self.dummy.prev = self.dummy
        self.n = 0

    def size(self):
        return DLList.size(self)

    # IMPORTANT: avoid recursion issues in tester printing
    def __str__(self):
        s = "["
        u = self.dummy.next
        i = 0
        while u is not self.dummy:
            s += "%r" % u.x
            u = u.next
            i += 1
            if i < self.n:
                s += ","
        return s + "]"

    __repr__ = __str__
