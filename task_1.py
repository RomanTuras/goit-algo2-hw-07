import random
import time
from functools import lru_cache
import copy

N = 100000
array = [random.randint(1, 100) for _ in range(N)]

Q = 50000
queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(("Range", L, R))
    else:
        idx = random.randint(0, N - 1)
        val = random.randint(1, 100)
        queries.append(("Update", idx, val))


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


array_copy = array.copy()


@lru_cache(maxsize=1000)
def range_sum_with_cache(L, R, array_snapshot):
    return sum(array_snapshot[L : R + 1])


def range_sum_wrapper(array, L, R):
    return range_sum_with_cache(L, R, tuple(array))


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


array_no_cache = copy.deepcopy(array)
array_with_cache = copy.deepcopy(array)


start = time.time()
for q in queries:
    if q[0] == "Range":
        range_sum_no_cache(array_no_cache, q[1], q[2])
    else:
        update_no_cache(array_no_cache, q[1], q[2])
end = time.time()
print(f"Час виконання без кешування: {end - start:.2f} секунд")


start = time.time()
for q in queries:
    if q[0] == "Range":
        range_sum_wrapper(array_with_cache, q[1], q[2])
    else:
        update_with_cache(array_with_cache, q[1], q[2])
end = time.time()
print(f"Час виконання з LRU-кешем: {end - start:.2f} секунд")


print("Статистика кешу:", range_sum_with_cache.cache_info())
