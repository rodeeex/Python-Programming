import timeit
import math
from functions import integrate_with_threads


def benchmark_threads(n_iter_parallel: int = 10000000):
    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_with_threads(math.sin, 0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} потока/ов: {t:.4f} сек.')


if __name__ == '__main__':
    benchmark_threads()
