from functools import lru_cache


def fact_recursive(n: int) -> int:
    """
    Вычислить факториал числа рекурсивно без мемоизации

    :param n: натуральное число или 0
    :return: факториал числа n
    :raises ValueError: число n меньше 0
    """
    if n < 0:
        raise ValueError('Для отрицательных чисел факториал не вычисляется')
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache(maxsize=None)
def fact_recursive_lru(n: int) -> int:
    """
    Вычислить факториал числа рекурсивно с мемоизацией

    :param n: натуральное число или 0
    :return: факториал числа n
    :raises ValueError: число n меньше 0
    """
    if n < 0:
        raise ValueError('Для отрицательных чисел факториал не вычисляется')
    if n == 0:
        return 1
    return n * fact_recursive_lru(n - 1)


def fact_iterative(n: int) -> int:
    """
    Вычислить факториал числа итеративно без мемоизации

    :param n: натуральное число или 0
    :return: факториал числа n
    :raises ValueError: число n меньше 0
    """
    if n < 0:
        raise ValueError('Для отрицательных чисел факториал не вычисляется')
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


@lru_cache(maxsize=None)
def fact_iterative_lru(n: int) -> int:
    """
    Вычислить факториал числа итеративно с мемоизацией

    :param n: натуральное число или 0
    :return: факториал числа n
    :raises ValueError: число n меньше 0
    """
    if n < 0:
        raise ValueError('Для отрицательных чисел факториал не вычисляется')
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result