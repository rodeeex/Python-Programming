import math
from typing import Callable


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    """
    Вычисление определённого интеграла функции f на отрезке [a, b] методом прямоугольников

    :param f: интегрируемая функция
    :param a: левая граница интервала
    :param b: правая граница интервала
    :param n_iter: количество разбиений
    :return: приближённое значение интеграла
    :raises ValueError: если a >= b или n_iter <= 0

    >>> abs(integrate(math.sin, 0, math.pi, n_iter=100000) - 2) < 1e-4
    True
    >>> abs(integrate(lambda x: x**2, 0, 1, n_iter=100000) - 1/3) < 1e-4
    True
    """
    if a >= b:
        raise ValueError('Левая граница должна быть меньше правой')
    if n_iter <= 0:
        raise ValueError('Количество итераций должно быть положительным')

    acc: float = 0.0
    step: float = (b - a) / n_iter
    half_step: float = step / 2

    for i in range(n_iter):
        acc += f(a + i * step + half_step) * step
    return acc
