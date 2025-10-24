import re
import unittest
from tree import BinTree


class TestBinTree(unittest.TestCase):
    def test_recursive_build(self):
        """
        Проверить корректность построения дерева по количеству его элементов
        """
        tree = BinTree(root_val=2.5, height=3, is_recursive=True)
        result = tree.convert('list')
        self.assertEqual(len(result), 2 ** 3 - 1)

    def test_non_recursive_build(self):
        """
        Проверить корректность НЕрекурсивного построения дерева по количеству его элементов
        """
        tree = BinTree(root_val=7, height=4, is_recursive=False)
        result = tree.convert('list')
        self.assertEqual(len(result), 2 ** 4 - 1)

    def test_invalid_function_signature(self):
        """
        В функцию нельзя поместить аргумент, не являющийся строго одним числом
        """
        with self.assertRaisesRegex(
                TypeError,
                re.compile(r'Функции для вычисления листьев должны принимать один аргумент float')
        ):
            BinTree(root_val=1, height=2,
                    count_left_leaf_function=lambda: 12432)

    def test_invalid_function_return_type(self):
        """
        Функции для вычисления листьев не должны возвращать что-либо, кроме числа
        """
        with self.assertRaisesRegex(
                TypeError,
                re.compile(r'Функции для вычисления листьев должны возвращать float, возвращено str')
        ):
            BinTree(root_val=1, height=2,
                    count_left_leaf_function=lambda x: 'rtherthert')

    def test_conversion_to_dict(self):
        """
        Преобразование в словарь должно выполняться корректно
        """
        tree = BinTree(root_val=-54, height=2, is_recursive=False,
                       count_left_leaf_function=lambda x: 2 * x + 1,
                       count_right_leaf_function=lambda x: 2 * x)
        expected = {
            'value': -54,
            'left': {
                "value": -107,
                "left": None,
                "right": None
            },
            'right': {
                'value': -108,
                'left': None,
                'right': None
            }
        }
        self.assertEqual(tree.convert('dict'), expected)

    def test_conversion_to_dict_recursive(self):
        """
        Рекурсивное преобразование в словарь должно выполняться корректно
        """
        tree = BinTree(root_val=1.25, height=3, is_recursive=True,
                       count_left_leaf_function=lambda x: 2 * x + 1,
                       count_right_leaf_function=lambda x: 2 * x)
        expected = {
            'value': 1.25,
            'left': {
                'value': 3.5,
                'left': {
                    'value': 8.0,
                    'left': None,
                    'right': None
                },
                'right': {
                    'value': 7.0,
                    'left': None,
                    'right': None
                }
            },
            'right': {
                'value': 2.5,
                'left': {
                    'value': 6.0,
                    'left': None,
                    'right': None
                },
                'right': {
                    'value': 5.0,
                    'left': None,
                    'right': None
                }
            }
        }
        self.assertEqual(tree.convert('dict_recursive'), expected)

    def test_convertion_to_list(self):
        """
        Преобразование в список должно выполняться корректно
        """
        tree = BinTree(root_val=5, height=5, is_recursive=False,
                       count_left_leaf_function=lambda x: x + 1,
                       count_right_leaf_function=lambda x: x + 2)
        result = tree.convert('list')
        self.assertEqual(result,
                         [5, 6, 7, 7, 8, 8, 9, 8, 9, 9, 10, 9, 10, 10, 11, 9, 10, 10, 11, 10, 11, 11, 12, 10, 11, 11,
                          12, 11, 12, 12, 13])

    def test_tree_from_one_root(self):
        """
        Дерево из одного корня должно создаваться и преобразовываться правильно
        """
        tree = BinTree(root_val=277.0, height=1)
        with self.subTest():
            self.assertEqual(tree.convert('list'), [277.0])
            self.assertEqual(tree.convert('dict'), {'value': 277.0, 'left': None, 'right': None})


if __name__ == '__main__':
    unittest.main()
