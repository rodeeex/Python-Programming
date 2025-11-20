import unittest
import io
from src.logger_dec import logger
from src.custom_exceptions import CriticalError, WarningMessage


class TestLoggerStream(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

    def test_success_logging(self):
        """
        Проверка нормальной работы функции
        """

        @logger(handle=self.stream)
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)
        self.assertEqual(result, 5)

        logs = self.stream.getvalue()

        self.assertIn("Начало вызова функции test_func", logs)
        self.assertIn("Функция test_func завершилась успешно", logs)
        self.assertIn("args=(2, 3)", logs)
        self.assertIn("Результат: 5", logs)

    def test_error_logging(self):
        """
        Логгер должен отловить тип ошибки (ERROR) и указать её в логах
        """

        @logger(handle=self.stream)
        def test_func(x):
            raise ValueError("Fake")

        with self.assertRaises(ValueError):
            test_func(10)

        logs = self.stream.getvalue()

        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Fake", logs)

    def test_warning_message_logging(self):
        """
        Предупреждение должно логироваться как WARNING
        """

        @logger(handle=self.stream)
        def test_func():
            raise WarningMessage("warn_error")

        with self.assertRaises(WarningMessage):
            test_func()

        logs = self.stream.getvalue()

        self.assertIn("WARNING", logs)
        self.assertIn("WarningMessage", logs)
        self.assertIn("warn_error", logs)

    def test_critical_error_logging(self):
        """
        Проверка детектирования критической ошибки в логах
        """

        @logger(handle=self.stream)
        def test_func():
            raise CriticalError("fatal_error")

        with self.assertRaises(CriticalError):
            test_func()

        logs = self.stream.getvalue()

        self.assertIn("CRITICAL", logs)
        self.assertIn("CriticalError", logs)
        self.assertIn("fatal_error", logs)

    def test_logging_error_from_assignment_example(self):
        """
        При запросе валюты с неправильного URL выбрасывается ConnectionError
        """

        @logger(handle=self.stream)
        def wrapped():
            from src.get_currencies import get_currencies
            return get_currencies(['USD'], url="https://invalid_url")

        with self.assertRaises(ConnectionError):
            wrapped()

        logs = self.stream.getvalue()

        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
