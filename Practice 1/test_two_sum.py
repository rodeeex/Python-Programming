import unittest
from two_sum import two_sum


class MyTestCase(unittest.TestCase):
    def test_empty_list(self):
        """
        В пустом списке пара индексов не найдётся
        """
        self.assertEqual(two_sum([], 277), None)

    def test_one_element(self):
        """
        В списке из одного элемента пара индексов не найдётся
        """
        self.assertEqual(two_sum([1], 7), None)

    def test_list_of_equal_elements(self):
        """
        В списке из одинаковых чисел вернётся наименьшая пара индексов
        """
        self.assertEqual(two_sum([0, 2, 2, 2, 2, 2], 4), (1, 2))

    def test_list_of_different_types(self):
        """
        Все нецелочисленные элементы пропускаются при подсчёте, даже если вещественные в сумме дают правильный ответ
        """
        self.assertEqual(two_sum([1, "abc", 1.5, 2, 6, 5.5, None, oct(123)], 7), (0, 4))

    def test_several_solutions(self):
        """
        В списке, где элементы разные, но решений несколько, вернётся наименьшая пара индексов
        """
        self.assertEqual(two_sum([1, 4, 2, 3], 5), (0, 1))

    def test_no_correct_elements(self):
        """
        Если целочисленные элементы отсутствуют в списке, то вернётся None
        """
        self.assertEqual(two_sum(["hello_world", "123123", 0.123, None], 54), None)

    def test_negative_elements(self):
        """
        Программа также должна возвращать корректную пару индексов и для отрицательных чисел
        """
        self.assertEqual(two_sum([0, 412, 67, -12, 4, 20, 4, 0], 8), (3, 5))


if __name__ == '__main__':
    unittest.main()
