import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


# ------------------- Splay Tree -------------------
class Node:
    def __init__(self, key, value=None, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
        elif key > current_node.key:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)
        else:
            current_node.value = value  # Update if key already exists

    def find(self, key):
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


# ------------------- Fibonacci functions -------------------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n < 2:
        tree.insert(n, n)
        return n

    cached = tree.find(n)
    if cached is not None:
        return cached

    val1 = tree.find(n - 1)
    if val1 is None:
        val1 = fibonacci_splay(n - 1, tree)

    val2 = tree.find(n - 2)
    if val2 is None:
        val2 = fibonacci_splay(n - 2, tree)

    result = val1 + val2
    tree.insert(n, result)
    return result


# ------------------- Benchmark & Plot -------------------
def benchmark():
    fib_values = list(range(0, 1000, 50))
    lru_times = []
    splay_times = []
    table_data = []

    for n in fib_values:
        # LRU Cache
        def stmt_lru():
            return fibonacci_lru(n)

        time_lru = timeit.timeit(stmt_lru, number=1)
        lru_times.append(time_lru)

        # Splay Tree
        tree = SplayTree()

        def stmt_splay():
            return fibonacci_splay(n, tree)

        time_splay = timeit.timeit(stmt_splay, number=1)
        splay_times.append(time_splay)

        table_data.append((n, time_lru, time_splay))

    # Table
    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
    print("-" * 60)
    for n, lru, splay in table_data:
        print(f"{n:<10}{lru:<25.10f}{splay:<25.10f}")

    # Chart
    plt.figure(figsize=(10, 6))
    plt.plot(fib_values, lru_times, marker="o", label="LRU Cache")
    plt.plot(fib_values, splay_times, marker="s", label="Splay Tree")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Time (seconds)")
    plt.title("Порівняння часу обчислення чисел Фібоначчі")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    benchmark()
