from typing import Iterable

import matplotlib.pyplot as plt


def plot_results(heights: Iterable[int], recursive_results: list[float], iterative_results: list[float]):
    """
    Построить график сравнения времени работы рекурсивного и нерекурсивного алгоритмов

    :param heights: список высот дерева
    :param recursive_results: результаты работы рекурсивного алгоритма
    :param iterative_results: результаты работы нерекурсивного алгоритма
    """
    plt.figure(figsize=(8, 5))
    plt.plot(heights, recursive_results, label='Рекурсивный алгоритм')
    plt.plot(heights, iterative_results, label='Нерекурсивный алгоритм')

    plt.title('Сравнение времени построения дерева')
    plt.xlabel('Высота')
    plt.ylabel('Время построения (сек.)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
