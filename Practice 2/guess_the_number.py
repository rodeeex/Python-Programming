"""
Решение с бинарным поиском имеет временную сложность O(log2(n)), а с медленным инкрементом - O(n)
Поскольку range в любом случае отдаст отсортированную последовательность, я решил формировать входной список
из случайных целых чисел в пределах диапазона и в кол-ве от половины длины диапазона до длины-1

TODO: написать документацию к функциям, проверить правильность аннотаций типов, написать тесты для обычного и бинарного поиска
"""
from typing import Literal, List, Tuple
import random

type search_algorithm = Literal['seq', 'bin']


def generate_random_list(start: int, end: int, size: int) -> List[int]:
    return random.sample(range(start, end + 1), size)


def helper() -> Tuple[int, int, int, search_algorithm]:
    target = int(input("Введите искомое число: "))
    start_range = int(input("Введите начало диапазона: "))
    end_range = int(input("Введите конец диапазона: "))
    algo = input("Введите алгоритм поиска (seq [по умолчанию] / bin): ")
    if algo != 'seq' and algo != 'bin' and algo != '':
        raise ValueError("Неверный алгоритм поиска. Введите правильное значение.")
    else:
        return target, start_range, end_range, algo


def guess_the_number(target: int, lst: List[int], algo: search_algorithm = 'seq') -> Tuple[int, int | None]:
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
    target, start_range, end_range, algo = helper()

    lst = generate_random_list(start_range, end_range,
                               random.randint((end_range - start_range) // 2, end_range - start_range - 1))
    lst = sorted(lst)

    result = guess_the_number(target, lst, algo=algo) if algo != '' else guess_the_number(target, lst)

    # print("Список: ", *lst)
    # print("Длина списка: ", len(lst))
    print("Результат: ", *result)


if __name__ == '__main__':
    main()
