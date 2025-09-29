# Примечание: в первых 4 тестах список я назвал диапазоном
# Тесты функции gueess_the_number() для seq и bin объединил в саб-тесты для удобства

import unittest

from guess_the_number import guess_the_number


class TestGuessTheNumber(unittest.TestCase):
    def test_number_in_range(self):
        """
        Искомое число входит в диапазон
        """
        lst = [10, 12, 23, 45, 54, 90]
        cases = [
            (54, 'seq', (54, 5)),
            (54, 'bin', (54, 2)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_number_not_in_range(self):
        """
        Искомое число НЕ входит в диапазон
        """
        lst = [23, 34, 987, 23453]
        cases = [
            (12, 'seq', (12, None)),
            (12, 'bin', (12, None)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_list_from_one_element(self):
        """
        Список состоит из одного элемента; программа должна отгадать число за одну попытку при любом алгоритме
        """
        lst = [5]
        cases = [
            (5, 'seq', (5, 1)),
            (5, 'bin', (5, 1)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_list_from_two_neighbour_elements(self):
        """
        Список состоит из двух соседних целых чисел
        """
        lst = [6, 7]
        cases = [
            (7, 'seq', (7, 2)),
            (7, 'bin', (7, 2))
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_empty_list(self):
        """
        Список для угадывания пустой; программа всегда должна возвращать вторым элементом кортежа None
        """
        lst = []
        cases = [
            (277, 'seq', (277, None)),
            (277, 'bin', (277, None)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_list_goes_through_zero(self):
        """
        Список для угадывания проходит через 0; программа должна корректно работать с отрицательными числами
        """
        lst = [-12, -9, -6, -1, 0, 4, 7, 16, 21]
        cases = [
            (4, 'seq', (4, 6)),
            (4, 'bin', (4, 3)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )

    def test_negative_list(self):
        """
        Список для угадывания состоит из отрицательных чисел; программа должна корректно работать с отрицательными числами
        """
        lst = [-27, -26, -20, -12, -11, -4, -3]
        cases = [
            (-4, 'seq', (-4, 6)),
            (-4, 'bin', (-4, 2)),
        ]
        for target, algo, expected in cases:
            with self.subTest(algo=algo):
                self.assertEqual(
                    guess_the_number(target, lst, algo=algo),
                    expected
                )
