from Interfaces import Graph, List
import numpy as np
from ArrayList import ArrayList
from ArrayStack import ArrayStack
from ArrayQueue import ArrayQueue


class AdjacencyList(Graph):
    def __init__(self, n: int, dtype=ArrayList):
        self.n = n
        self.dtype = dtype
        self.adj = np.zeros(n, dtype=self.dtype)
        for i in range(self.n):
            self.adj[i] = self.dtype()

    def _check_vertex(self, v: int):
        if v < 0 or v >= self.n:
            raise IndexError(f"Vertex index {v} is out of bounds for graph of size {self.n}.")

    def add_edge(self, i: int, j: int):
        """
        adds a directed edge from node i to node j
        """
        self._check_vertex(i)
        self._check_vertex(j)

        # avoid duplicates
        if not self.has_edge(i, j):
            self.adj[i].append(j)

    def remove_edge(self, i: int, j: int):
        """
        removes the directed edge from node i to node j,
        if it exists in the graph. Returns True if removed, False otherwise.
        """
        self._check_vertex(i)
        self._check_vertex(j)

        lst = self.adj[i]
        for k in range(lst.size()):
            if lst.get(k) == j:
                lst.remove(k)
                return True
        return False

    def has_edge(self, i: int, j: int) -> bool:
        """
        determines if the directed edge from node i to node j exists
        """
        self._check_vertex(i)
        self._check_vertex(j)

        lst = self.adj[i]
        for k in range(lst.size()):
            if lst.get(k) == j:
                return True
        return False

    def out_edges(self, i) -> List:
        """
        returns a List of all nodes j such that (i, j) is an edge
        """
        self._check_vertex(i)

        out = self.dtype()
        lst = self.adj[i]
        for k in range(lst.size()):
            out.append(lst.get(k))
        return out

    def in_edges(self, j) -> List:
        """
        returns a List of all nodes i such that (i, j) is an edge
        """
        self._check_vertex(j)

        inc = self.dtype()
        for i in range(self.n):
            if self.has_edge(i, j):
                inc.append(i)
        return inc

    def bfs(self, r: int):
        """
        Breadth-First Search traversal starting at r.
        Returns a List of visited node indices in visit order.
        """
        self._check_vertex(r)

        visited = [False] * self.n
        order = self.dtype()

        q = ArrayQueue()
        q.add(r)
        visited[r] = True

        while q.size() > 0:
            u = q.remove()
            order.append(u)

            nbrs = self.adj[u]
            for k in range(nbrs.size()):
                v = nbrs.get(k)
                if not visited[v]:
                    visited[v] = True
                    q.add(v)

        return order

    def dfs(self, r: int):
        """
        Depth-First Search traversal starting at r.
        Returns a List of visited node indices in visit order.
        """
        self._check_vertex(r)

        visited = [False] * self.n
        order = self.dtype()

        st = ArrayStack()
        st.push(r)

        while st.size() > 0:
            u = st.pop()
            if visited[u]:
                continue

            visited[u] = True
            order.append(u)

            # push neighbors in reverse so DFS matches "natural" left-to-right order
            nbrs = self.adj[u]
            for k in range(nbrs.size() - 1, -1, -1):
                v = nbrs.get(k)
                if not visited[v]:
                    st.push(v)

        return order

    def size(self):
        return self.n

    def __str__(self):
        s = ""
        for i in range(0, self.n):
            s += f"{i}:  {self.adj[i]}\n"
        return s
