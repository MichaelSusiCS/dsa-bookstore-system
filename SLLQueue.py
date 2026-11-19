from Interfaces import Queue


class SLLQueue(Queue):
    class Node:
        def __init__(self, x: object):
            self.next = None
            self.x = x

    def __init__(self):
        """
        constructor; initializes an empty SLLQueue
        """
        self.head = None
        self.tail = None
        self.n = 0

    def add(self, x: object):
        """
        adds an element to the tail of the queue
        """
        u = SLLQueue.Node(x)
        if self.n == 0:
            self.head = u
            self.tail = u
        else:
            self.tail.next = u
            self.tail = u
        self.n += 1

    def remove(self) -> object:
        """
        removes and returns the head of the queue
        :raises: IndexError if empty
        """
        if self.n == 0:
            raise IndexError()
        x = self.head.x
        self.head = self.head.next
        self.n -= 1
        if self.n == 0:
            self.tail = None
        return x

    def reverse(self):
        """
        reverses the order of the queue
        """
        prev = None
        curr = self.head
        self.tail = self.head  # old head becomes new tail
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def size(self) -> int:
        return self.n

    def __str__(self):
        s = "["
        u = self.head
        while u is not None:
            s += "%r" % u.x
            u = u.next
            if u is not None:
                s += ","
        return s + "]"

    __repr__ = __str__

    # IMPORTANT: makes MaxQueue iterable for BookStore.cartBestSeller()
    def __iter__(self):
        self.iterator = self.head
        return self

    def __next__(self):
        if self.iterator is not None:
            x = self.iterator.x
            self.iterator = self.iterator.next
            return x
        raise StopIteration()
