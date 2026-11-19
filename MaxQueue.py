from SLLQueue import SLLQueue
from DLLDeque import DLLDeque


class MaxQueue(SLLQueue):
    def __init__(self):
        SLLQueue.__init__(self)
        self.max_deque = DLLDeque()

    def add(self, x: object):
        SLLQueue.add(self, x)

        if self.max_deque.size() == 0:
            self.max_deque.add_first(x)
            return

        # if x is bigger than current max, clear and set
        if x > self.max_deque.get(0):
            self.max_deque.clear()
            self.max_deque.add_first(x)
            return

        # pop smaller elements from the back
        while self.max_deque.size() > 0 and self.max_deque.get(self.max_deque.size() - 1) < x:
            self.max_deque.remove_last()

        self.max_deque.add_last(x)

    def remove(self) -> object:
        r = SLLQueue.remove(self)
        if self.max_deque.size() > 0 and r == self.max_deque.get(0):
            self.max_deque.remove_first()
        return r

    def max(self):
        if self.max_deque.size() == 0:
            raise IndexError()
        return self.max_deque.get(0)

    __repr__ = SLLQueue.__str__
