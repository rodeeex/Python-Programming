import timeit
import math
from functions.integrate import integrate


def benchmark_first_iteration():
    print('Итерация 1 (замеры базовой версии)\n')

    n_iter_values = [1000, 10000, 100000, 1000000]

    for n in n_iter_values:
        stmt = f'integrate(math.sin, 0, math.pi, n_iter={n})'
        t = timeit.timeit(stmt, globals=globals(), number=10)
        result = integrate(math.sin, 0, math.pi, n_iter=n)
        print(f'n_iter = {n}: {t:.4f} сек., результат прибл. = {result:.10f}')


if __name__ == '__main__':
    benchmark_first_iteration()
