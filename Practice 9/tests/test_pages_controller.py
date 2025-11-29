import unittest
from unittest.mock import MagicMock
from jinja2 import Environment, DictLoader
from controllers.pages_controller import PagesController


class TestPagesController(unittest.TestCase):

    def setUp(self):
        env = Environment(loader=DictLoader({
            'index.html': '<h1>{{ app.name }}</h1>',
            'currencies.html': '{% for c in currencies %}{{ c.char_code }}{% endfor %}'
        }))
        self.controller = PagesController(
            env=env,
            currency_controller=MagicMock()
        )

    def test_render_index(self):
        """
        Проверка рендеринга главной страницы
        """
        mock_app = MagicMock()
        mock_app.name = 'TestApp'
        mock_author = MagicMock()
        mock_currencies = MagicMock()
        mock_author.name = 'Test'

        html = self.controller.render_index(app=mock_app, currencies=mock_currencies, author=mock_author)
        self.assertIn('<h1>TestApp</h1>', html)

    def test_render_currencies(self):
        """
        Проверка рендеринга списка валют
        """
        mock_currency = MagicMock()
        mock_currency.char_code = 'USD'
        self.controller.currency_controller.list_currencies.return_value = [mock_currency]

        html = self.controller.render_currencies(currencies=[mock_currency])
        self.assertIn('USD', html)