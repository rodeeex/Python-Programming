"""
Решение с бинарным поиском имеет временную сложность O(log2(n)), а с медленным инкрементом - O(n).

Поскольку range в любом случае отдаст отсортированную последовательность, я для разнообразия решил формировать входной
список из случайных целых чисел в пределах диапазона и в кол-ве от половины длины диапазона до полной его длины
и уже потом его сортировать.
"""
from typing import Literal, List, Tuple
import random

type search_algorithm = Literal['seq', 'bin']


def generate_random_list(start: int, end: int, size: int) -> List[int]:
    """
    Сгенерировать список уникальных случайных целых чисел в определённом количестве в заданном диапазоне (включительно).

    Аргументы:
    :param start: начало диапазона
    :param end: конец диапазона
    :param size: количество чисел в списке
    :return: список целых чисел
    """
    return random.sample(range(start, end + 1), size)


def helper() -> Tuple[int, int, int, search_algorithm]:
    """
    Обработать ввод с клавиатуры и вернуть введённые значения.

    :return: кортеж из 4 введённых с клавиатуры значений
    :raise ValueError: введено некорректное значение (число не целое или алгоритм поиска неверный)

    Примечание: если начальное значение диапазона больше конечного, поменять их местами.
    """
    try:
        target = int(input('Введите искомое число: '))
        start_range = int(input('Введите начало диапазона: '))
        end_range = int(input('Введите конец диапазона: '))
    except ValueError:
        raise ValueError('Одно или несколько чисел не являются целыми')

    if start_range > end_range:
        start_range, end_range = end_range, start_range

    algo = input('Введите алгоритм поиска (seq [по умолчанию] / bin): ')
    if algo not in {'seq', 'bin', ''}:
        raise ValueError('Неверный алгоритм поиска. Введите правильное значение (seq [по умолчанию], bin).')
    else:
        return target, start_range, end_range, algo


def guess_the_number(target: int, lst: List[int], algo: search_algorithm = 'seq') -> Tuple[int, int | None]:
    """
    Угадать заданное число среди приведённого отсортированного списка с заданным алгоритмом угадывания.

    :param target: число, которое нужно угадать
    :param lst: список, в котором требуется найти число
    :param algo: алгоритм угадывания числа: медленный инкремент ('seq', по умолчанию) / бинарный поиск ('bin')
    :return: кортеж из искомого числа и количества попыток его угадывания (кол-во попыток - None, если число не найдено)
    """
    attempts = 0
    found = False
    if algo == 'seq':
        for i in range(len(lst)):
            attempts += 1
            if lst[i] == target:
                found = True
                break
    elif algo == 'bin':
        left, right = 0, len(lst) - 1
        while left <= right:
            mid = (left + right) // 2
            attempts += 1
            if lst[mid] == target:
                found = True
                break
            elif lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
    return target, attempts if found else None


def main():
    """
    Инициализировать переменные для угадывания числа, вызвав функцию helper().
    Сгенерировать список случайных значений с помощью функции generate_random_list(), затем его отсортировать.
    Вывести результат.

    Примечания:

    В качестве нижней границы кол-ва чисел в генерируемом списке выступает половина длины диапазона (или 1),
    а в качестве верхней границы - его длина.

    Если строка algo - пустая, вызывать guess_the_number() с последним аргументом по умолчанию.
    """
    target, start_range, end_range, algo = helper()

    lst = generate_random_list(start_range, end_range,
                               random.randint(max(1, (end_range - start_range + 1) // 2), end_range - start_range + 1))
    lst = sorted(lst)

    result = guess_the_number(target, lst, algo=algo) if algo != '' else guess_the_number(target, lst)

    print('Результат: ', *result)


if __name__ == '__main__':
    main()
