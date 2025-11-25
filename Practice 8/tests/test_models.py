import unittest
from models import Author, App, User, Currency, UserCurrency


class TestAuthor(unittest.TestCase):
    def test_valid_author(self):
        """
        Проверка корректного создания автора
        """
        author = Author('Антон', 'P4150')
        self.assertEqual(author.name, 'Антон')
        self.assertEqual(author.group, 'P4150')

    def test_invalid_name(self):
        """
        Проверка исключения при пустом имени
        """
        with self.assertRaises(ValueError):
            Author('', 'P4150')
        with self.assertRaises(ValueError):
            Author('   ', 'P4150')

    def test_invalid_group(self):
        """
        Проверка исключения при некорректной группе
        """
        with self.assertRaises(ValueError):
            Author('Антон', 123)


class TestUser(unittest.TestCase):
    def test_valid_user(self):
        """
        Проверка корректного создания пользователя
        """
        user = User(1, 'Антон')
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Антон')

    def test_invalid_id(self):
        """
        Проверка возникновения исключения при отрицательном ID
        """
        with self.assertRaises(ValueError):
            User(0, 'Антон')
        with self.assertRaises(ValueError):
            User(-5, 'Антон')


class TestCurrency(unittest.TestCase):
    def test_valid_currency(self):
        """
        Проверка корректного создания валюты
        """
        curr = Currency(1, '840', 'USD', 'Доллар США', 75.5, 1)
        self.assertEqual(curr.char_code, 'USD')
        self.assertEqual(curr.value, 75.5)

    def test_invalid_char_code(self):
        """
        Проверка неверного кода валюты
        """
        with self.assertRaises(ValueError):
            Currency(1, '840', 'US1', 'Доллар', 75.5, 1)

    def test_invalid_nominal(self):
        """
        Проверка исключения при ситуации, когда номинал не может быть нулевым
        """
        with self.assertRaises(ValueError):
            Currency(1, '840', 'USD', 'Доллар', 75.5, 0)


class TestApp(unittest.TestCase):
    def test_valid_app(self):
        """
        Проверка корректного создания приложения
        """
        author = Author('Bruh', 'P4150')
        app = App('TestApp', '1.0', author)
        self.assertEqual(app.name, 'TestApp')
        self.assertEqual(app.author, author)

    def test_invalid_author_type(self):
        """
        Проверка типа автора
        """
        with self.assertRaises(TypeError):
            App('TestApp', '1.0', 'щшаощшуцаоцущша')
