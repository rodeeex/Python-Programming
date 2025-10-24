import timeit
from typing import Iterable

from tree import BinTree


def build_tree_recursive(height: int):
    """
    Построить дерево рекурсивным методом

    :param height: высота дерева
    """
    BinTree(height=height, is_recursive=True)


def build_tree_iterative(height: int):
    """
    Построить дерево нерекурсивным методом

    :param height: высота дерева
    """
    BinTree(height=height, is_recursive=False)


def benchmark(heights: Iterable[int], number: int = 100) -> tuple[list[float], list[float]]:
    """
    Измерить время работы двух способов построения дерева (высота при этом увеличивается)

    :param heights: список высот
    :param number: кол-во повторений замеров (по умолчанию 100)
    :return: кортеж из двух списков с результатами для, соответственно, рекурсивного и нерекурсивного построения
    """
    recursive_results = []
    iterative_results = []

    for i in heights:
        rec_time = timeit.timeit(lambda: build_tree_recursive(i), number=number)
        iter_time = timeit.timeit(lambda: build_tree_iterative(i), number=number)
        recursive_results.append(rec_time / number)
        iterative_results.append(iter_time / number)

    return recursive_results, iterative_results