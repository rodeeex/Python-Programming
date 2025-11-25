import unittest
from unittest.mock import patch, Mock
from utils.currencies_api import get_currency_data
from requests.exceptions import RequestException


class TestGetCurrencyData(unittest.TestCase):

    @patch('utils.currencies_api.requests.get')
    def test_success(self, mock_get):
        """
        Успешное получение данных
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            'Valute': {
                'USD': {
                    'NumCode': '840', 'CharCode': 'USD', 'Nominal': 1,
                    'Name': 'Доллар США', 'Value': 75.5
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_currency_data(['USD'])
        self.assertEqual(result['USD']['CharCode'], 'USD')
        self.assertEqual(result['USD']['Value'], 75.5)

    @patch('utils.currencies_api.requests.get')
    def test_currency_not_found(self, mock_get):
        """
        Валюта отсутствует в ответе
        """
        mock_response = Mock()
        mock_response.json.return_value = {'Valute': {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_currency_data(['TON'])
        self.assertIsNone(result['TON'])

    @patch('utils.currencies_api.requests.get')
    def test_connection_error(self, mock_get):
        """
        Ошибка подключения
        """

        mock_get.side_effect = RequestException('Проблемы с сетью')
        with self.assertRaises(ConnectionError):
            get_currency_data(['USD'])

    @patch('utils.currencies_api.requests.get')
    def test_invalid_json(self, mock_get):
        """
        Некорректный JSON-ответ от API
        """
        mock_response = Mock()
        mock_response.json.side_effect = ValueError('Некорректный JSON')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_currency_data(['USD'])
