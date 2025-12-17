import timeit
import math
from functions import integrate, integrate_with_threads, integrate_with_processes
from Practice10.functions.c_integrate import integrate_sin, integrate_sin_with_threads, integrate_sin_with_processes
from Practice10.functions.c_integrate_nogil import integrate_sin_nogil_threads


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
        print(f'{j} потока/ов: {t:.4f} сек.')


def benchmark_third_iteration(n_iter_parallel: int = 10000000):
    print('\nИтерация 3 (оптимизация через процессы)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_with_processes(math.sin, 0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} процесса/ов: {t:.4f} сек.')


def benchmark_fourth_iteration():
    print('\nИтерация 4 (Cython без потоков)\n')

    n_iter_values = [1000, 10000, 100000, 1000000, 10000000]

    for n in n_iter_values:
        stmt = f'integrate_sin(0, math.pi, n_iter={n})'
        t = timeit.timeit(stmt, globals=globals(), number=10)
        print(f'n_iter = {n}: {t:.4f} сек.')


def benchmark_fourth_iteration_with_threads(n_iter_parallel: int = 10000000):
    print('\nИтерация 4 (Cython с потоками)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_sin_with_threads(0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} потока/ов: {t:.4f} сек.')


def benchmark_fourth_iteration_with_processes(n_iter_parallel: int = 10000000):
    print('\nИтерация 4 (Cython с процессами)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_sin_with_processes(0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} процесса/ов: {t:.4f} сек.')


def benchmark_fifth_iteration_nogil(n_iter_parallel: int = 10000000):
    print('\nИтерация 5 (Cython с nogil и потоками через prange)\n')

    jobs = [2, 4, 6, 8]

    for j in jobs:
        stmt = f'integrate_sin_nogil_threads(0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} потока/ов (nogil): {t:.4f} сек.')


def benchmark_fifth_iteration_comparison(n_iter_parallel: int = 10000000):
    print('\nИтерация 5 (сравнение nogil-потоков с Cython-процессами)\n')

    jobs = [2, 4, 6, 8]

    print('С nogil-потоками:')
    for j in jobs:
        stmt = f'integrate_sin_nogil_threads(0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} потока/ов: {t:.4f} сек.')

    print('\nС Cython-процессами:')
    for j in jobs:
        stmt = f'integrate_sin_with_processes(0, math.pi, n_jobs={j}, n_iter={n_iter_parallel})'
        t = timeit.timeit(stmt, globals=globals(), number=5)
        print(f'{j} процесса/ов: {t:.4f} сек.')


if __name__ == '__main__':
    benchmark_first_iteration()
    benchmark_second_iteration()
    benchmark_third_iteration()
    benchmark_fourth_iteration()
    benchmark_fourth_iteration_with_threads()
    benchmark_fourth_iteration_with_processes()
    benchmark_fifth_iteration_nogil()
    benchmark_fifth_iteration_comparison()
