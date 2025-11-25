import unittest
from http.server import HTTPServer
from threading import Thread
import urllib.request
from myapp import MyRequestHandler


class TestServerRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 5051
        cls.server = HTTPServer(('', cls.port), MyRequestHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _fetch(self, path: str) -> str:
        url = f'http://localhost:{self.port}{path}'
        with urllib.request.urlopen(url) as r:
            return r.read().decode('utf-8')

    def test_root(self):
        """
        Проверка главной страницы
        """
        html = self._fetch('/')
        self.assertIn('<h1>CurrenciesApp', html)
        self.assertIn('Антон Пушкарев', html)

    def test_users(self):
        """
        Проверка списка пользователей
        """
        html = self._fetch('/users')
        self.assertIn('rodex', html)
        self.assertIn('techno', html)

    def test_user_id_valid(self):
        """
        Проверка страницы пользователя
        """
        html = self._fetch('/user?id=1')
        self.assertIn('rodex', html)
        self.assertIn('USD', html)

    def test_user_id_invalid(self):
        """
        Некорректный ID должен привести к ошибке 400
        """
        with self.assertRaises(urllib.request.HTTPError) as cm:
            self._fetch('/user?id=fake')
        self.assertEqual(cm.exception.code, 400)

    def test_404(self):
        """
        Несуществующий маршрут должен выдавать ошибку 404
        """
        with self.assertRaises(urllib.request.HTTPError) as cm:
            self._fetch('/fwefwefwefwe')
        self.assertEqual(cm.exception.code, 404)
