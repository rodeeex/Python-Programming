from jinja2 import Environment
from models.author import Author
from controllers.currency_crud import CurrencyController

class PagesController:
    def __init__(self, env: Environment, currency_controller: CurrencyController):
        self.env = env
        self.currency_controller = currency_controller

    def render_currencies(self) -> str:
        currencies = self.currency_controller.list_currencies()
        template = self.env.get_template("currencies.html")
        return template.render(currencies=currencies)

    def render_index(self, author: Author) -> str:
        template = self.env.get_template("index.html")
        return template.render(author=author)