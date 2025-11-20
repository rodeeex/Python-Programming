import unittest
import io
from src.logger_dec import logger
from src.custom_exceptions import WarningMessage


class TestLogger(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

    def test_logging_success(self):
        @logger(handle=self.stream)
        def fac(x):
            counter = 1
            for i in range(1, x + 1):
                counter *= i
            return counter

        result = fac(5)
        self.assertEqual(result, 120)

        logs = self.stream.getvalue()
        self.assertIn("Начало вызова функции fac", logs)
        self.assertIn("завершилась успешно", logs)
        self.assertIn("args=(5,)", logs)
        self.assertIn("Результат: 120", logs)

    def test_logging_error(self):
        @logger(handle=self.stream)
        def error(x):
            raise ValueError("ERROR")

        with self.assertRaises(ValueError):
            error(123)

        logs = self.stream.getvalue()
        self.assertRegex(logs, "ERROR")
        self.assertIn("ValueError", logs)

    def test_logging_warning_message(self):
        @logger(handle=self.stream)
        def warning_message():
            raise WarningMessage("WARNING")

        with self.assertRaises(WarningMessage):
            warning_message()

        logs = self.stream.getvalue()
        self.assertIn("WARNING", logs)
        self.assertIn("WarningMessage", logs)
