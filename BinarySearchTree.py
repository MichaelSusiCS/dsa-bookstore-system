from BinaryTree import BinaryTree
from Interfaces import Set


class BinarySearchTree(BinaryTree, Set):

    def __init__(self):
        BinaryTree.__init__(self)
        self.n = 0

    def add(self, key: object, value: object = None) -> bool:
        if self.r is None:
            self.r = BinaryTree.Node(key, value)
            self.n += 1
            return True
        p = self._find_last(key)
        if key == p.k:
            return False
        u = BinaryTree.Node(key, value)
        return self._add_child(p, u)

    def find(self, key: object) -> object:
        u = self._find_eq(key)
        return None if u is None else u.v

    def remove(self, key: object):
        u = self._find_eq(key)
        if u is None:
            raise ValueError(f"{key} not found.")
        x = u.v
        self._remove_node(u)
        return x

    def _find_eq(self, key: object) -> BinaryTree.Node:
        u = self.r
        while u is not None:
            if key < u.k:
                u = u.left
            elif key > u.k:
                u = u.right
            else:
                return u
        return None

    def _find_last(self, key: object) -> BinaryTree.Node:
        u = self.r
        prev = None
        while u is not None:
            prev = u
            if key < u.k:
                u = u.left
            elif key > u.k:
                u = u.right
            else:
                return u
        return prev

    def _add_child(self, p: BinaryTree.Node, u: BinaryTree.Node) -> bool:
        if u.k < p.k:
            p.left = u
        else:
            p.right = u
        u.parent = p
        self.n += 1
        return True

    def _splice(self, u: BinaryTree.Node):
        if u.left is not None:
            s = u.left
        else:
            s = u.right

        if u == self.r:
            self.r = s
            if s is not None:
                s.parent = None
        else:
            p = u.parent
            if p.left == u:
                p.left = s
            else:
                p.right = s
            if s is not None:
                s.parent = p

    def _remove_node(self, u: BinaryTree.Node):
        if u.left is None or u.right is None:
            self._splice(u)
        else:
            w = u.right
            while w.left is not None:
                w = w.left
            u.k = w.k
            u.v = w.v
            self._splice(w)
        self.n -= 1

    def clear(self):
        self.r = None
        self.n = 0

    def bookstore_helper(self, prefix: str):
        u = self.r
        while u is not None:
            if u.k.startswith(prefix):
                return u
            elif prefix < u.k:
                u = u.left
            else:
                u = u.right
        return None

    def __iter__(self):
        u = self.first_node()
        while u is not None:
            yield u.k
            u = self.next_node(u)

    def first_node(self):
        w = self.r
        if w is None: return None
        while w.left is not None:
            w = w.left
        return w

    def next_node(self, w):
        if w.right is not None:
            w = w.right
            while w.left is not None:
                w = w.left
        else:
            while w.parent is not None and w.parent.left != w:
                w = w.parent
            w = w.parent
        return w
