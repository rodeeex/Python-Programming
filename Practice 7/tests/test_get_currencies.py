import unittest
from src.get_currencies import get_currencies


class TestGetCurrencies(unittest.TestCase):

    def test_real_currencies(self):
        """
        Проверка возврата реальных курсов валют
        """
        data = get_currencies(["USD", "EUR"])
        self.assertIn("USD", data)
        self.assertIn("EUR", data)

        self.assertIsInstance(data["USD"], float)
        self.assertIsInstance(data["EUR"], float)

    def test_nonexistent_currency(self):
        """
        Валюта отсутствует в отдаваемом JSON-документе
        """
        data = get_currencies(["KVA"])
        self.assertIn("KVA", data)
        self.assertIn("не найден", data["KVA"])

    def test_connection_error(self):
        """
        Если API недоступен, должна выбрасываться ConnectionError
        """
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://erferwergerge")

    def test_invalid_json(self):
        """
        Если формат JSON-документ некорректен, должна вывестись ValueError
        """
        with self.assertRaises(ValueError):
            get_currencies(["USD"], url="https://google.com")