from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from typing import Callable
from .integrate import integrate


def integrate_with_processes(f: Callable[[float], float], a: float, b: float, *,
                             n_jobs: int = 2, n_iter: int = 1000) -> float:
    """
    Вычисление интеграла с помощью процессов через ProcessPoolExecutor

    :param f: интегрируемая функция
    :param a: левая граница
    :param b: правая граница
    :param n_jobs: количество процессов
    :param n_iter: общее количество итераций
    :return: приближённое значение интеграла
    """

    executor = ProcessPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(f.result() for f in as_completed(fs))
