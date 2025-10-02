import unittest
from io import StringIO
from unittest.mock import patch
from main import helper


class TestHelper(unittest.TestCase):
    @patch("builtins.input", side_effect=["10", "3", "y", "y", "y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_valid_input_all_custom_params(self, mock_stdout, mock_input):
        """
        Введённые параметры должны корректно парситься в словарь
        """
        params, use_recursive_dict = helper()
        with self.subTest():
            self.assertEqual(params['root_val'], 10)
            self.assertEqual(params['height'], 3)
            self.assertIn('count_left_leaf_function', params)
            self.assertIn('count_right_leaf_function', params)
            self.assertTrue(use_recursive_dict)

    @patch("builtins.input", side_effect=["", "", "n", "y", "y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_default_empty_inputs(self, mock_stdout, mock_input):
        """
        Возможно использование параметров: высоты, длины, и функций листьев по умолчанию (как это определено в самом дереве)
        """
        params, use_recursive_dict = helper()
        with self.subTest():
            self.assertNotIn('root_val', params)
            self.assertNotIn('height', params)
            self.assertNotIn('count_left_leaf_function', params)
            self.assertNotIn('count_right_leaf_function', params)
            self.assertTrue(use_recursive_dict)

    @patch("builtins.input", side_effect=["peorjkg09v", "5", "y", "y", "y"])
    def test_invalid_root_value(self, mock_input):
        """
        Если корень не является числом, при его вводе выбросится исключение
        """
        with self.assertRaises(ValueError, msg="Неверное значение! Корень дерева - это вещественное число."):
            helper()

    @patch("builtins.input", side_effect=["5", "-277", "y", "y", "y"])
    def test_invalid_height(self, mock_input):
        """
        Высота дерева не должна быть меньше 1, иначе выбросится исключение
        """
        with self.assertRaises(ValueError, msg="Неверное значение! Высота дерева не может быть меньше 1."):
            helper()

    @patch("builtins.input", side_effect=["5", "3", "ff34rf", "y", "y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_custom_function_choice(self, mock_stdout, mock_input):
        """
        Для выбора функций листьев нельзя ввести значения, кроме y и n, иначе выбросится исключение
        """
        with self.assertRaises(ValueError,
                               msg="Неверное значение! Использовать определённые в файле функции - y, оставить стандартные - n."):
            helper()

    @patch("builtins.input", side_effect=["5", "3", "y", "f34f34", "y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_recursive_choice(self, mock_stdout, mock_input):
        """
        Для выбора рекурсии при построении дерева нельзя ввести значения, кроме y и n, иначе выбросится исключение
        """
        with self.assertRaises(ValueError,
                               msg="Неверное значение! Использовать рекурсию при построении дерева - y, не использовать - n."):
            helper()

    @patch("builtins.input", side_effect=["5", "3", "y", "y", "ccccc"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_recursive_dict_choice(self, mock_stdout, mock_input):
        """
        Для выбора рекурсии при выводе дерева через словарь нельзя ввести значения, кроме y и n, иначе выбросится исключение
        """
        with self.assertRaises(ValueError,
                               msg="Неверное значение! Использовать рекурсию при ВЫВОДЕ дерева - y, не использовать - n."):
            helper()


if __name__ == "__main__":
    unittest.main()
