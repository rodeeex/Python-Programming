import math
from typing import Tuple, Optional
from .custom_exceptions import CriticalError, WarningMessage


def solve_quadratic(a: float, b: float, c: float) -> Optional[Tuple[float, ...]]:
    """
    Решает квадратное уравнение ax^2 + bx + c = 0

    :param a: коэффициент a
    :param b: коэффициент b
    :param c: свободный член
    :returns: кортеж корней или None
    :raises TypeError: a, b, c не числа
    :raises ValueError: a == 0
    :raises Warning: дискриминант < 0
    :raises CriticalError: a == 0 и b == 0
    """
    for name, value in zip(('a', 'b', 'c'), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Коэффициент {name} должен быть числом, получено: {value}')

    if a == 0 and b == 0:
        raise CriticalError(f'Невозможно решить уравнение: a = 0 и b=0')

    if a == 0:
        raise ValueError('Коэффициент a не может быть равен 0')

    d = b * b - 4 * a * c

    if d < 0:
        raise WarningMessage(f'Дискриминант < 0: уравнение {a}x^2 + {b}x + {c} не имеет действительных корней')
    elif d == 0:
        return (-b / (2 * a),)
    else:
        root1 = (-b + math.sqrt(d)) / (2 * a)
        root2 = (-b - math.sqrt(d)) / (2 * a)
        return root1, root2
