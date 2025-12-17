from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from typing import Callable
from .integrate import integrate


def integrate_with_threads(f: Callable[[float], float], a: float, b: float, *,
                           n_jobs: int = 2, n_iter: int = 1000) -> float:
    """
    Асинхронное вычисление интеграла с помощью потоков (ThreadPoolExecutor)

    :param f: интегрируемая функция
    :param a: левая граница
    :param b: правая граница
    :param n_jobs: количество потоков
    :param n_iter: общее количество итераций
    :return: приближённое значение интеграла
    """
    executor = ThreadPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(f.result() for f in as_completed(fs))
