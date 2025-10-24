import timeit
from typing import List, Callable, Tuple


def benchmark(numbers: List[int], first_function: Callable[[int], int], second_function: Callable[[int], int],
              num_runs: int = 5000) -> Tuple[List[float], List[float]]:
    """
    Провести бенчмарк двух функций для вычисления факториала.
    Измерить время выполнения для каждого числа n.

    :param numbers: список входных чисел для тестирования
    :param first_function: первая функция для бенчмарка
    :param second_function: вторая функция для бенчмарка
    :param num_runs: количество замеров времени работы одной функции
    :return: кортеж из двух списков с результатами работы первой и второй функций
    """
    first_results = []
    second_results = []

    for n in numbers:
        curr_time_1 = timeit.timeit(lambda: first_function(n), number=num_runs) / num_runs
        first_results.append(curr_time_1)
        curr_time_2 = timeit.timeit(lambda: second_function(n), number=num_runs) / num_runs
        second_results.append(curr_time_2)

    return first_results, second_results
