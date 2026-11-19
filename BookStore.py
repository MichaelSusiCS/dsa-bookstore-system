import sys
import traceback
import time

import AdjacencyList
import AdjacencyMatrix
import algorithms
import ArrayList
import DLList
import ChainedHashTable
from exceptions import InvalidStateException
import BinaryHeap
import BinarySearchTree
import BinaryTree
from Book import Book
import MaxQueue
from SortableBook import SortableBook


class BookStore:
    """
    Simulates a book system such as Amazon. It allows searching,
    removing and adding to a shopping cart.
    """

    def __init__(self):
        self.bookCatalog = None
        self.shoppingCart = MaxQueue.MaxQueue()
        self.mapKeysToIdxs = None
        self.mapTitlesToIdxs = None
        self.booksByRank = None
        self.catalogIsSorted = None
        self.similarityGraph = None
        self.dtype = None

    """ --------- METHODS RELATED TO THE CATALOG --------- """

    def load_catalog(self, fileName: str, catalog_ds: str, graph_ds: str, sort_by: str):
        """
        Loads the catalog, optionally sorts it, builds key/title maps, and builds similarity graph.
        """
        self.mapTitlesToIdxs = BinarySearchTree.BinarySearchTree()
        self.catalogIsSorted = False
        msg = ""

        try:
            # choose catalog list type
            if catalog_ds == '1':
                self.dtype = ArrayList.ArrayList
                msg += "- ArrayList catalog selected.  "
            elif catalog_ds == '2':
                self.dtype = DLList.DLList
                msg += "- DLList catalog selected.  "
            else:
                raise ValueError(f"'{catalog_ds}' is not a valid catalog data structure option.")

            self.bookCatalog = self.dtype()
            self.mapKeysToIdxs = ChainedHashTable.ChainedHashTable(self.dtype)

            # begin loading catalog
            start_time = time.time()
            with open(fileName, encoding="utf8") as f:
                for line in f:
                    (key, title, group, rank, similar) = line.split("^")
                    s = SortableBook(key, title.strip(), group, rank, similar)
                    self.bookCatalog.append(s)

            # sorting catalog
            if sort_by == '1':
                algorithms.quick_sort(self.bookCatalog)  # random pivot default
                self.catalogIsSorted = True
                msg += "\n- Catalog was sorted with quick-sort, random pivot.  "
            elif sort_by == '2':
                algorithms.quick_sort(self.bookCatalog, False)  # first pivot
                self.catalogIsSorted = True
                msg += "\n- Catalog was sorted with quick_sort, first-element pivot.  "
            else:
                msg += "\n- Invalid sorting algorithm selected. Catalog was not sorted."

            elapsed_time = time.time() - start_time

            # loading dictionaries
            for i in range(self.bookCatalog.size()):
                book = self.bookCatalog.get(i)
                self.mapKeysToIdxs.add(book.key, i)              # (key -> index)
                self.mapTitlesToIdxs.add(book.title.lower(), i)  # (title -> index)

            n = self.bookCatalog.size()

            # loading graph
            if graph_ds == '1':
                # Adjacency List
                self.similarityGraph = AdjacencyList.AdjacencyList(n, self.dtype)
                msg += "\n- Graph: AdjacencyList selected.  "
            elif graph_ds == '2':
                # Adjacency Matrix
                self.similarityGraph = AdjacencyMatrix.AdjacencyMatrix(n, self.dtype)
                msg += "\n- Graph: AdjacencyMatrix selected.  "
            else:
                raise ValueError(f"'{graph_ds}' is not a valid graph data structure option.")

            # build edges from "similar" keys
            m = 0
            for source_node in range(self.bookCatalog.size()):
                book = self.bookCatalog.get(source_node)
                similar = book.similar.split(" ")

                # first token is usually count; skip it + remove empties
                similar = [x for x in similar[1:] if len(x) > 0]

                for key in similar:
                    if '\n' in key:
                        key = key.replace('\n', '')

                    # index of the similar book
                    target_node = self.mapKeysToIdxs.find(key)

                    if target_node is not None:
                        self.similarityGraph.add_edge(source_node, target_node)
                        m += 1

            print(
                "\nLoad Summary:\n"
                + msg
                + f"\n- Loaded and sorted {n} items."
                + f"\n- Created graph with {n} nodes and {m} edges."
                + f"\nAction completed in {elapsed_time} seconds."
            )

        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def get_book_at_index(self, i: int):
        try:
            start_time = time.time()
            book = self.bookCatalog.get(i)
            elapsed_time = time.time() - start_time
            print(f"Accessed the following book from catalog:{book}")
            print(f"\nAction completed in {elapsed_time} seconds.")
        except IndexError:
            print(f"Index {i} is out of bounds for catalog of size {self.bookCatalog.size()}")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def search_by_infix(self, infix: str, n: int, by_rank: bool):
        if not by_rank:
            try:
                printed = 0
                start_time = time.time()
                for i in range(self.bookCatalog.size()):
                    book = self.bookCatalog.get(i)
                    if infix.lower() in book.title.lower():
                        print("-" * 25 + f"\nMatch found at catalog index {i}:\n{book}\n")
                        printed += 1
                    if printed == n:
                        break
                elapsed_time = time.time() - start_time
                print(f"Found {printed} matches in {elapsed_time} seconds.")
            except Exception:
                print("The following unexpected error occurred:")
                traceback.print_exc(limit=2, file=sys.stdout)
        else:
            try:
                start_time = time.time()
                self.booksByRank = BinaryHeap.BinaryHeap()
                for i in range(self.bookCatalog.size()):
                    book = self.bookCatalog.get(i)
                    if infix.lower() in book.title.lower():
                        b = Book(book.key, book.title, book.group, -1 * book.rank, book.group)
                        self.booksByRank.add(b)

                printed = 0
                for _ in range(self.booksByRank.size()):
                    top_book = self.booksByRank.remove()
                    top_book.rank = abs(top_book.rank)
                    print("-" * 25 + f"\nTop Match #{printed + 1}:\n{top_book}\n")
                    printed += 1
                    if printed == n:
                        break

                elapsed_time = time.time() - start_time
                print(f"Found {printed} matches in {elapsed_time} seconds.")
            except Exception:
                print("The following unexpected error occurred:")
                traceback.print_exc(limit=2, file=sys.stdout)

    def search_by_title(self, title: str, search_algo):
        try:
            if search_algo == '1':
                start_time = time.time()
                idx = algorithms.linear_search(self.bookCatalog, title)
                elapsed_time = time.time() - start_time
            elif search_algo == '2':
                if self.catalogIsSorted:
                    start_time = time.time()
                    idx = algorithms.binary_search(self.bookCatalog, title)
                    elapsed_time = time.time() - start_time
                else:
                    raise InvalidStateException("Cannot perform Binary Search on unsorted catalog.")
            else:
                raise ValueError("Invalid searching algorithm was selected.  Please try again.")

            if idx is None:
                print(f"\nThe title \"{title}\" does not exist in the catalog.")
            else:
                print("-" * 40 + f"\nThe following book matching the given title was found at catalog index {idx}:{self.bookCatalog.get(idx)}")
            print(f"Action completed in {elapsed_time} seconds.")

        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def search_by_key(self, key):
        try:
            start_time = time.time()
            idx = self.mapKeysToIdxs.find(key)
            elapsed_time = time.time() - start_time
            if idx is None:
                print(f"\nThere is no book with key \"{key}\" in the catalog.")
            else:
                print(f"\nThe following book matching the given key was found at catalog index {idx}:{self.bookCatalog.get(idx)}")
            print(f"\nAction completed in {elapsed_time} seconds.")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)
        return

    def search_by_prefix(self, prefix, n):
        lowercase_prefix = prefix.lower()
        try:
            start_time = time.time()
            r = self.mapTitlesToIdxs.bookstore_helper(lowercase_prefix)
            printed = 0
            if r is None:
                print(f"\nThere are no titles that begin with \"{prefix}\" in the catalog.")
            else:
                bt = BinaryTree.BinaryTree()
                bt.r = r
                nodes = ArrayList.ArrayList(bt.bf_order())
                algorithms.merge_sort(nodes)
                for i in range(len(nodes)):
                    idx = nodes[i].v
                    book = self.bookCatalog.get(idx)
                    if lowercase_prefix == book.title[0:len(prefix)].lower():
                        print('-' * 20 + f"\nMatch #{printed + 1} at index {idx}:\n{book}")
                        printed += 1
                    if n == printed:
                        break
            elapsed_time = time.time() - start_time
            print(f"\nFound {printed} matches in {elapsed_time} seconds.")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)
        return

    """ --------- METHODS RELATED TO THE SHOPPING CART --------- """

    def add_book_at_index(self, i: int):
        try:
            start_time = time.time()
            s = self.bookCatalog.get(i)
            self.shoppingCart.add(s)
            elapsed_time = time.time() - start_time
            print(f"\nAdded to shopping cart: {s}")
            self._display_similar(i)
            print(f"\nAction completed in {elapsed_time} seconds.")
        except IndexError:
            print(f"Index {i} is out of bounds for catalog of size {self.bookCatalog.size()}")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def add_book_with_key(self, key):
        try:
            start_time = time.time()
            i = self.mapKeysToIdxs.find(key)
            if i is not None:
                s = self.bookCatalog.get(i)
                self.shoppingCart.add(s)
                elapsed_time = time.time() - start_time
                print(f"\nAdded to shopping cart: {s}")
                self._display_similar(i)
                print(f"\nAction completed in {elapsed_time} seconds.")
            else:
                print(f"The key '{key}' does not exist in the catalog")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def remove_from_shopping_cart(self):
        try:
            start_time = time.time()
            if self.shoppingCart.size() > 0:
                u = self.shoppingCart.remove()
                elapsed_time = time.time() - start_time
                print(f"Removed from shopping cart the following book:\n{u}\nAction completed in {elapsed_time} seconds.")
            else:
                elapsed_time = time.time() - start_time
                print(f"Nothing to remove.  Shopping cart is empty.\nAction completed in {elapsed_time} seconds.")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    def cart_best_seller(self):
        try:
            if self.shoppingCart.size() > 0:
                start_time = time.time()
                bestseller = self.shoppingCart.max()
                elapsed_time = time.time() - start_time
                print("All books in shopping cart:")
                for book in self.shoppingCart:
                    print('-' * 10 + str(book))
                print('-' * 30 + f"\nThe highest ranking book:{bestseller}\nAction completed in {elapsed_time} seconds")
            else:
                print("Shopping cart is empty.")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)

    """ HELPER METHOD """

    def _display_similar(self, idx: int):
        """
        Displays items at most TWO edges away (outgoing edges) from idx.
        That means:
          - all out-neighbors of idx (distance 1)
          - all out-neighbors of those neighbors (distance 2)
        """
        try:
            similar = self.dtype()

            if self.similarityGraph is None:
                return

            n = self.bookCatalog.size()
            visited = [False] * n
            visited[idx] = True

            # distance 1
            level1 = self.similarityGraph.out_edges(idx)
            for k in range(level1.size()):
                v = level1[k]
                if 0 <= v < n and not visited[v]:
                    visited[v] = True
                    similar.append(v)

            # distance 2
            for k in range(level1.size()):
                u = level1[k]
                if 0 <= u < n:
                    level2 = self.similarityGraph.out_edges(u)
                    for t in range(level2.size()):
                        v = level2[t]
                        if 0 <= v < n and not visited[v]:
                            visited[v] = True
                            similar.append(v)

            if similar.size() > 0:
                print(f"\nYou might also like:")
                print('-' * 100)
                print("%-15s | %-15s | %-15s | %-100s |" % ('Key', 'Index', 'Group', 'Title'))
                print('-' * 100)
                for i in range(similar.size()):
                    sim_idx = similar[i]
                    similar_book = self.bookCatalog.get(sim_idx)
                    print("%-15s | %-15s | %-15s | %-100s |" % (
                        similar_book.key, sim_idx, similar_book.group, similar_book.title))

        except IndexError:
            print(f"Index {idx} is out of bounds for catalog of size {self.bookCatalog.size()}")
        except Exception:
            print("The following unexpected error occurred:")
            traceback.print_exc(limit=2, file=sys.stdout)
