import unittest
from unittest.mock import MagicMock
from controllers.user_currency_controller import UserCurrencyController
from models.currency import Currency


class TestUserCurrencyController(unittest.TestCase):
    def test_subscribe_to_currency(self):
        """
        Проверка создания подписки пользователя на валюту
        """
        mock_uc_db = MagicMock()
        mock_uc_db.create.return_value = 101
        controller = UserCurrencyController(
            user_crud=MagicMock(),
            user_currency_crud=mock_uc_db,
            currency_crud=MagicMock()
        )

        sub_id = controller.subscribe_to_currency(user_id=5, currency_id=3)

        self.assertEqual(sub_id, 101)
        mock_uc_db.create.assert_called_once_with(5, 3)

    def test_get_user_subscriptions(self):
        """
        Проверка получения списка валют, на которые подписан пользователь
        """
        mock_uc_db = MagicMock()
        mock_uc_db.read_user_currencies.return_value = [
            (1, '840', 'USD', 'Доллар США', 75.5, 1),
            (2, '978', 'EUR', 'Евро', 82.1, 1)
        ]
        controller = UserCurrencyController(
            user_crud=MagicMock(),
            user_currency_crud=mock_uc_db,
            currency_crud=MagicMock()
        )

        currencies = controller.get_user_subscriptions(5)

        self.assertEqual(len(currencies), 2)
        self.assertIsInstance(currencies[0], Currency)
        self.assertEqual(currencies[0].char_code, 'USD')
        self.assertEqual(currencies[1].char_code, 'EUR')
        mock_uc_db.read_user_currencies.assert_called_once_with(5)
