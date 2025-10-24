import random
from typing import List
import matplotlib.pyplot as plt


def generate_random_numbers(size: int) -> List[int]:
    """
    Сгенерировать список уникальных случайных чисел в диапазоне [100; 300), отсортированный по возрастанию

    :param size: количество чисел для генерации
    :return: отсортированный список случайных чисел
    """
    numbers = random.sample(range(100, 300), size)
    numbers.sort()
    return numbers

def draw_plot(numbers: List[int], first_results: List[float], second_results: List[float], label1: str, label2: str,
              title: str):
    """
    Построить график сравнения времени выполнения двух функций.
    Создаёт график: по оси абсцисс - числа, для которых вычисляется факториал, а по оси ординат — среднее время выполнения.

    :param numbers: список чисел, для которых вычисляется факториал
    :param first_results: список результатов выполнения первой функции (в секундах)
    :param second_results: список результатов выполнения второй функции (в секундах)
    :param label1: подпись для первого графика
    :param label2: подпись для второго графика
    :param title: заголовок
    :return: None
    """
    plt.figure(figsize=(10, 5))
    plt.plot(numbers, first_results, label=label1)
    plt.plot(numbers, second_results, label=label2)
    plt.xlabel('Входное число n')
    plt.ylabel('Среднее время выполнения')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
