import timeit
import math
from functions import integrate, integrate_with_threads, integrate_with_processes


def benchmark_first_iteration():
    print('Итерация 1 (замеры базовой версии)\n')

    n_iter_values = [1000, 10000, 100000, 1000000, 10000000]

    for n in n_iter_values:
        stmt = f'integrate(math.sin, 0, math.pi, n_iter={n})'
        t = timeit.timeit(stmt, globals=globals(), number=10)
        print(f'n_iter = {n}: {t:.4f} сек.')


def benchmark_second_iteration(n_iter_parallel: int = 10000000):
    print('\nИтерация 2 (оптимизация через потоки)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_with_threads(math.sin, 0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} потоков: {t:.4f} сек.')


def benchmark_third_iteration(n_iter_parallel: int = 10000000):
    print('\nИтерация 3 (оптимизация через процессы)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_with_processes(math.sin, 0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} процессов: {t:.4f} сек.')


if __name__ == '__main__':
    benchmark_first_iteration()
    benchmark_second_iteration()
    benchmark_third_iteration()
