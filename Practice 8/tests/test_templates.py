import unittest
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency


class TestTemplates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env = Environment(
            loader=PackageLoader('myapp'),
            autoescape=select_autoescape()
        )

    def test_index_template(self):
        """
        Проверка рендеринга главной страницы
        """
        author = Author('Антон Пушкарев', 'P4150')
        app = App('CurrenciesApp', '1.0', author)

        template = self.env.get_template('index.html')
        html = template.render(myapp=app, author=author)

        self.assertIn('<h1>CurrenciesApp', html)
        self.assertIn('Антон Пушкарев', html)
        self.assertIn('P4150', html)
        self.assertIn('href="/"', html)
        self.assertIn('href="/users"', html)

    def test_users_template(self):
        """
        Проверка списка пользователей и цикла
        """
        users = [
            User(1, 'rodex'),
            User(2, 'techno')
        ]

        template = self.env.get_template('users.html')
        html = template.render(users=users)

        self.assertIn('rodex', html)
        self.assertIn('techno', html)
        self.assertIn('href="/user?id=1"', html)
        self.assertIn('href="/user?id=2"', html)

        html_empty = template.render(users=[])
        self.assertIn('Нет пользователей', html_empty)

    def test_currencies_template(self):
        """
        Проверка таблицы валют и цикла
        """
        currencies = [
            Currency(1, '840', 'USD', 'Доллар США', 77.9556, 1),
            Currency(2, '978', 'EUR', 'Евро', 90.5903, 1)
        ]

        template = self.env.get_template('currencies.html')
        html = template.render(currencies=currencies)

        self.assertIn('USD', html)
        self.assertIn('Евро', html)
        self.assertIn('77.9556', html)
        self.assertIn('90.5903', html)
        self.assertIn('<td>1</td>', html)

        html_empty = template.render(currencies=[])
        self.assertIn('Нет данных', html_empty)

    def test_user_template_with_subscriptions(self):
        """
        Проверка страницы пользователя с подписками
        """
        user = User(1, 'rodex')
        subscriptions = [
            Currency(1, '840', 'USD', 'Доллар США', 77.9556, 1),
            Currency(2, '978', 'EUR', 'Евро', 90.5903, 1)
        ]

        template = self.env.get_template("user.html")
        html = template.render(
            user=user,
            subscriptions=subscriptions,
            historical_data={}
        )

        self.assertIn("rodex", html)
        self.assertIn("USD", html)
        self.assertIn("Евро", html)
        self.assertIn("77.9556", html)

    def test_user_template_no_subscriptions(self):
        """
        Проверка сообщения при отсутствии подписок
        """
        user = User(1, "rodex")
        template = self.env.get_template("user.html")
        html = template.render(user=user, subscriptions=[], historical_data={})

        self.assertIn("rodex", html)
        self.assertIn("не подписан", html)

    def test_author_template(self):
        """
        Проверка страницы автора
        """
        author = Author("Антон Пушкарев", "P4150")
        app = App("CurrenciesApp", "1.0", author)

        template = self.env.get_template("author.html")
        html = template.render(author=author, app=app)

        self.assertIn("Антон Пушкарев", html)
        self.assertIn("P4150", html)
