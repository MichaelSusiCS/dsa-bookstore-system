from Interfaces import Graph, List
from ArrayList import ArrayList
from ArrayQueue import ArrayQueue
from ArrayStack import ArrayStack
import numpy as np


class AdjacencyMatrix(Graph):

    def __init__(self, n: int, dtype=ArrayList):
        self.n = n
        self.adj = np.zeros((self.n, self.n), dtype=int)
        self.dtype = dtype

    def _check_vertex(self, v: int):
        if v < 0 or v >= self.n:
            raise IndexError(f"Vertex index {v} is out of bounds for graph of size {self.n}.")

    def add_edge(self, i: int, j: int):
        """
        adds a directed edge from node i to node j
        """
        self._check_vertex(i)
        self._check_vertex(j)
        self.adj[i][j] = 1

    def remove_edge(self, i: int, j: int):
        """
        removes the directed edge from node i to node j
        """
        self._check_vertex(i)
        self._check_vertex(j)
        if self.adj[i][j] == 1:
            self.adj[i][j] = 0
            return True
        return False

    def has_edge(self, i: int, j: int) -> bool:
        """
        determines if the directed edge from node i to node j exists
        """
        self._check_vertex(i)
        self._check_vertex(j)
        return self.adj[i][j] == 1

    def out_edges(self, i) -> List:
        """
        returns a List of node indices j such that (i, j) is an edge
        """
        self._check_vertex(i)
        out = self.dtype()
        for j in range(self.n):
            if self.adj[i][j] == 1:
                out.append(j)
        return out

    def in_edges(self, j) -> List:
        """
        returns a List of node indices i such that (i, j) is an edge
        """
        self._check_vertex(j)
        inc = self.dtype()
        for i in range(self.n):
            if self.adj[i][j] == 1:
                inc.append(i)
        return inc

    def bfs(self, r: int):
        """
        Breadth-First Search traversal
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

            for v in range(self.n):
                if self.adj[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    q.add(v)

        return order

    def dfs(self, r: int):
        """
        Depth-First Search traversal
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

            # reverse order to match expected DFS behavior
            for v in range(self.n - 1, -1, -1):
                if self.adj[u][v] == 1 and not visited[v]:
                    st.push(v)

        return order

    def size(self):
        return self.n

    def __str__(self):
        s = ""
        for i in range(0, self.n):
            s += f"{i}:  {self.adj[i]}\n"
        return s
