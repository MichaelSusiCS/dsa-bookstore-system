# Data Structures & Algorithms Library + Bookstore System (Python)

Fourteen data structures and the core search and sort algorithms, implemented from scratch in Python. They power a command-line bookstore over a 27,134-book catalog. I built it across the module projects of CECS 274 (Data Structures) at CSULB in Fall 2025.

## Data structures

All of these are implemented by hand. Array-based structures use NumPy arrays only as fixed-size backing storage.

| Category | Structures |
|---|---|
| Lists | `ArrayList` (array-backed, resizes by doubling), `DLList` (doubly linked) |
| Stacks, queues, deques | `ArrayStack`, `ArrayQueue`, `SLLStack`, `SLLQueue`, `DLLDeque`, `MaxQueue` |
| Hashing | `ChainedHashTable` |
| Trees | `BinaryTree`, `BinarySearchTree`, `BinaryHeap` |
| Graphs | `AdjacencyList`, `AdjacencyMatrix`, each with BFS and DFS |

**Algorithms** (`algorithms.py`): linear search, binary search, merge sort, and quicksort with a random or first-element pivot.

**Calculator** (`Calculator.py`): stores variables in the hash table, checks for balanced parentheses with a stack, and evaluates expressions such as `((x+y)*x)` by building a parse tree.

## Bookstore features (`BookStore.py`)

- **Load and sort:** loads the catalog into an `ArrayList` or `DLList`, then sorts it with quicksort.
- **Key lookup:** a `ChainedHashTable` maps each book key to its catalog index.
- **Title search:** linear or binary search over the sorted catalog.
- **Prefix search:** a `BinarySearchTree` maps titles to indexes, so all titles starting with a prefix can be found.
- **Top-ranked results:** a `BinaryHeap` ranks the books whose titles contain a search term.
- **Similar books:** a graph links each book to the books listed as similar. For `books_1.txt` that's 27,134 nodes and 3,671 edges.
- **Shopping cart:** add and remove books, and look up the cart's best seller.
- **Timing:** every operation prints how long it took. I used this to compare the array-based and linked designs.

## Run it

```bash
pip install numpy
python3 main.py
```

Choose the bookstore menu, load `books_1.txt`, and pick the data structures to use. With all 27,134 books, choose `AdjacencyList` for the graph: `AdjacencyMatrix` needs n² memory.

## Credits

The course provided starter code: `Interfaces.py`, `main.py`, `tester.py`, `Book.py`, `SortableBook.py`, and the `books_*.txt` catalog data. The data structure implementations, the algorithms, and the `BookStore` logic are mine.

When I combined the module projects into this repo, I made a few small fixes:
- `main.py` now imports `BookStore` instead of a missing module.
- Some helper methods from the final module's starter code were missing from my implementations, so I added them: list indexing, tree-node comparisons, and BST in-order iteration.
- `Book` now supports `<=` and `>=` comparisons, which the heap needs.
