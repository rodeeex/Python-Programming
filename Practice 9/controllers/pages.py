from jinja2 import Environment
from models.author import Author
from models.app import App
from models.user import User
from models.currency import Currency
from typing import List
from controllers.currency_crud import CurrencyController


class PagesController:
    def __init__(
            self,
            env: Environment,
            currency_controller: CurrencyController
    ):
        self.env = env
        self.currency_controller = currency_controller

    def render_index(self, app: App, author: Author, currencies: List[Currency]) -> str:
        """
        Рендерит главную страницу

        :param app: объект приложения
        :param author: объект автора
        :param currencies: список валют
        :return: HTML-строка
        """
        template = self.env.get_template('index.html')
        return template.render(app=app, author=author, currencies=currencies)

    def render_author(self, author: Author, app: App) -> str:
        """
        Рендерит страницу об авторе

        :param author: объект автора
        :param app: объект приложения
        :return: HTML-строка
        """
        template = self.env.get_template('author.html')
        return template.render(author=author, app=app)

    def render_users(self, users: List[User]) -> str:
        """
        Рендерит список пользователей

        :param users: список пользователей
        :return: HTML-строка
        """
        template = self.env.get_template('users.html')
        return template.render(users=users)

    def render_user(self, user: User, subscriptions: List[Currency]) -> str:
        """
        Рендерит страницу пользователя с подписками

        :param user: объект пользователя
        :param subscriptions: список валют, на которые подписан пользователь
        :return: HTML-строка
        """
        template = self.env.get_template("user.html")
        return template.render(user=user, subscriptions=subscriptions)

    def render_currencies(self, currencies: List[Currency]) -> str:
        """
        Рендерит список всех валют

        :param currencies: список валют
        :return: HTML-строка
        """
        template = self.env.get_template('currencies.html')
        return template.render(currencies=currencies)