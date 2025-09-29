import unittest

from unittest.mock import patch
from guess_the_number import helper


class TestHelper(unittest.TestCase):
    @patch('builtins.input')
    def test_inverted_range_seq(self, mock_input):
        """
        Если введённое начальное значение диапазона больше конечного, они меняются местами (для инкремента)
        """
        mock_input.side_effect = ['6', '123', '1', 'seq']
        expected = (6, 1, 123, 'seq')
        self.assertEqual(helper(), expected)

    @patch('builtins.input')
    def test_inverted_range_bin(self, mock_input):
        """
        Если введённое начальное значение диапазона больше конечного, они меняются местами (для бинарного поиска)
        """
        mock_input.side_effect = ['6', '123', '1', 'bin']
        expected = (6, 1, 123, 'bin')
        self.assertEqual(helper(), expected)

    @patch('builtins.input')
    def test_inverted_range_empty_algo(self, mock_input):
        """
        Если введённое начальное значение диапазона больше конечного, они меняются местами
        (для пустого значения алгоритма)
        """
        mock_input.side_effect = ['6', '123', '1', '']
        expected = (6, 1, 123, '')
        self.assertEqual(helper(), expected)

    @patch('builtins.input')
    def test_invalid_target_in_helper(self, mock_input):
        """
        Если ввести неверное число для угадывания, программа выкинет ValueError
        """
        mock_input.side_effect = ['rtgrtghrt', '10', '20', 'seq']
        with self.assertRaisesRegex(ValueError, 'Одно или несколько чисел не являются целыми'):
            helper()

    @patch('builtins.input')
    def test_invalid_start_in_helper(self, mock_input):
        """
        Если ввести неверное начало диапазона, программа выкинет ValueError
        """
        mock_input.side_effect = ['15', 'rtgrtghrt', '20', 'seq']
        with self.assertRaisesRegex(ValueError, 'Одно или несколько чисел не являются целыми'):
            helper()

    @patch('builtins.input')
    def test_invalid_end_in_helper(self, mock_input):
        """
        Если ввести неверный конец диапазона, программа выкинет ValueError
        """
        mock_input.side_effect = ['15', '10', 'rtgrtghrt', 'seq']
        with self.assertRaisesRegex(ValueError, 'Одно или несколько чисел не являются целыми'):
            helper()

    @patch('builtins.input')
    def test_invalid_algo_in_helper(self, mock_input):
        mock_input.side_effect = ['456', '10', '457', 'dfkjsdlkfjsldkf']
        with self.assertRaisesRegex(ValueError,
                                    r'Неверный алгоритм поиска\. Введите правильное значение \(seq \[по умолчанию\], bin\)\.'):
            helper()