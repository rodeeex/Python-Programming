import unittest
from unittest.mock import MagicMock
from controllers.currency_controller import CurrencyController
from models.currency import Currency


class TestCurrencyController(unittest.TestCase):

    def test_list_currencies(self):
        """
        Проверка получения списка всех валют
        """
        mock_currency = MagicMock(spec=Currency)
        type(mock_currency).id = 1
        type(mock_currency).char_code = 'USD'

        mock_crud = MagicMock()
        mock_crud.read.return_value = [mock_currency]

        controller = CurrencyController(crud=mock_crud)

        currencies = controller.list_currencies()

        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0].char_code, 'USD')
        mock_crud.read.assert_called_once()

    def test_update_currency(self):
        """
        Проверка обновления курса валюты
        """
        mock_crud = MagicMock()
        controller = CurrencyController(crud=mock_crud)

        controller.update_currency('USD', 76.0)

        mock_crud.update.assert_called_once_with('USD', 76.0)

    def test_delete_currency(self):
        """
        Проверка удаления валюты по ID
        """
        mock_crud = MagicMock()
        controller = CurrencyController(crud=mock_crud)

        controller.delete_currency(42)

        mock_crud.delete.assert_called_once_with(42)

    def test_create_currency(self):
        """
        Проверка создания новой валюты
        """
        mock_crud = MagicMock()
        mock_crud.create.return_value = 99
        controller = CurrencyController(crud=mock_crud)

        currency_id = controller.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=75.5,
            nominal=1
        )

        self.assertEqual(currency_id, 99)
        mock_crud.create.assert_called_once_with('840', 'USD', 'Доллар США', 75.5, 1)