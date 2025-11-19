import math
from typing import Tuple, Optional


def solve_quadratic(a: float, b: float, c: float) -> Optional[Tuple[float, ...]]:
    """
    Решает квадратное уравнение ax^2 + bx + c = 0

    :param a: коэффициент a
    :param b: коэффициент b
    :param c: свободный член
    :returns: кортеж корней
    :raises TypeError: если a, b, c не числа
    :raises ValueError: если a == 0
    """
    for name, value in zip(('a', 'b', 'c'), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Коэффициент {name} должен быть числом, получено: {value}')

    if a == 0:
        raise ValueError('Коэффициент a не может быть равен 0')

    d = b * b - 4 * a * c

    if d < 0:
        return None
    elif d == 0:
        return (-b / (2 * a),)
    else:
        root1 = (-b + math.sqrt(d)) / (2 * a)
        root2 = (-b - math.sqrt(d)) / (2 * a)
        return root1, root2
