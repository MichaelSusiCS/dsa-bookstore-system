from Interfaces import Set
from DLList import DLList
import numpy as np


class ChainedHashTable(Set):
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, listType=DLList):
        """
        initializes an empty table so that each bin holds a list
        of the given type
        :param listType: object type; the data type of the List;
                      defaults to DLList if dtype is not specified
        """
        self.lstType = listType
        self.d = 1
        self.t = self._alloc_table(2 ** self.d)
        self.z = 193759204821
        self.w = 31
        self.n = 0

    def _alloc_table(self, n: int):
        """
        helper method; creates a table with a given
        number of bins and given list type
        :param n: int type; the number of bins in the table
        """
        t = np.zeros(n, dtype=object)
        for i in range(n):
            t[i] = self.lstType()
        return t

    def _hash(self, key: object) -> int:
        """
        helper method; computes the hash value (i.e. bin number) for the given key
        """
        return self.z * hash(key) % (2 ** self.w) >> (self.w - self.d)

    # ------- small compatibility helpers (DLList/ArrayList/etc.) -------
    def _list_size(self, lst) -> int:
        try:
            return len(lst)
        except Exception:
            return lst.size()

    def _list_get(self, lst, i: int):
        try:
            return lst[i]
        except Exception:
            return lst.get(i)

    def _list_add_last(self, lst, x):
        # Prefer append if it exists, else add at size()
        if hasattr(lst, "append"):
            lst.append(x)
        else:
            lst.add(self._list_size(lst), x)

    # ------------------------------------------------------------------

    def find(self, key: object) -> object:
        """
        finds the value corresponding to the given key
        :param key: object type; the key of the item to search for
        :returns: object type; the value corresponding to the key, if the key exists
                  otherwise, returns None
        """
        b = self._hash(key)
        bucket = self.t[b]
        m = self._list_size(bucket)

        for i in range(m):
            node = self._list_get(bucket, i)
            if node.key == key:
                return node.value
        return None

    def add(self, key: object, value: object):
        """
        adds the given key-value pair to the table, if the key does not already exist
        in the table.
        :param key: object type; the key of the item to add
        :param value: object type; the value of the item to add
        :returns: True if the value was successfully added; False if key already exists and
                  new item was not added
        """
        b = self._hash(key)
        bucket = self.t[b]
        m = self._list_size(bucket)

        # if key already exists, do not add
        for i in range(m):
            node = self._list_get(bucket, i)
            if node.key == key:
                return False

        # add new node to end of bucket list
        self._list_add_last(bucket, ChainedHashTable.Node(key, value))
        self.n += 1

        # grow if #elements == #bins
        if self.n == len(self.t):
            self.resize()

        return True

    def remove(self, key: int) -> object:
        """
        if the key exists, removes the item with the given key and returns its value;
        otherwise returns None
        :param key: object type; the key of the item to remove
        :returns: object type or None type;
        """
        b = self._hash(key)
        bucket = self.t[b]
        m = self._list_size(bucket)

        for i in range(m):
            node = self._list_get(bucket, i)
            if node.key == key:
                val = node.value
                bucket.remove(i)
                self.n -= 1

                # shrink if table is too empty (keep at least 2 bins)
                if len(self.t) >= 3 * max(1, self.n) and self.d > 1:
                    self.resize()

                return val

        return None

    def resize(self):
        """
        resizes the table to double the number of bins if the current number of
        bins is the same as the number of elements; otherwise resizes to half the
        number of bins
        """
        old_t = self.t
        old_bins = len(old_t)

        # Decide new d based on load
        if self.n == old_bins:
            self.d += 1
        else:
            # shrink (but never below 2 bins => d >= 1)
            if self.d > 1:
                self.d -= 1
            else:
                return  # already minimal

        self.t = self._alloc_table(2 ** self.d)

        # rehash all nodes into new table
        for i in range(old_bins):
            bucket = old_t[i]
            m = self._list_size(bucket)
            for j in range(m):
                node = self._list_get(bucket, j)
                b = self._hash(node.key)
                self._list_add_last(self.t[b], node)

    def size(self) -> int:
        """
        returns the number of items in the table
        :returns: int type;
        """
        return self.n

    def set(self, key, new_value):
        """
        replaces the value of the given key
        :param key: object type; the key of the item to modify
        :param new_value: object type;
        :return: object type; the old value corresponding to key that was replaced
        :raises: ValueError if the given key does not exist in the table
        """
        b = self._hash(key)
        bucket = self.t[b]
        m = self._list_size(bucket)

        for i in range(m):
            node = self._list_get(bucket, i)
            if node.key == key:
                old_val = node.value
                node.value = new_value
                return old_val

        raise ValueError("Key does not exist in table")

    def get_keys(self):
        """
        returns a list of all keys stored in the table
        :returns: Python list object
        """
        keys = []
        for i in range(len(self.t)):
            bucket = self.t[i]
            m = self._list_size(bucket)
            for j in range(m):
                node = self._list_get(bucket, j)
                keys.append(node.key)
        return keys

    def __str__(self):
        """
        returns a string representation of the table with key-value items
        in format (key, value)
        :returns: str type;
        """
        s = "\n"
        for i in range(len(self.t)):
            s += str(i) + " : "
            for j in range(len(self.t[i])):
                k = self.t[i][j]  # jth node at ith list
                s += "(" + str(k.key) + ", " + str(k.value) + "); "
            s += "\n"
        return s
