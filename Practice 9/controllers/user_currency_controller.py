from typing import List

from controllers.currency_db import CurrencyDB
from controllers.user_currency_db import UserCurrencyDB
from controllers.user_db import UserDB
from models import Currency


class UserCurrencyController:
    def __init__(self, user_crud: UserDB, user_currency_crud: UserCurrencyDB, currency_crud: CurrencyDB):
        self.user_crud = user_crud
        self.user_currency_crud = user_currency_crud
        self.currency_crud = currency_crud

    def subscribe_to_currency(self, user_id: int, currency_id: int) -> int:
        """
        Подписать пользователя на валюту

        :param user_id: ID пользователя
        :param currency_id: ID валюты
        :return: ID созданной привязки в БД
        """
        return self.user_currency_crud.create(user_id, currency_id)

    def get_user_subscriptions(self, user_id: int) -> List[Currency]:
        """
        Получить список валют, на которые подписан пользователь

        :param user_id: ID пользователя
        :return: список объектов Currency
        """
        rows = self.user_currency_crud.read_user_currencies(user_id)
        return [
            Currency(
                id_=r[0],
                num_code=r[1],
                char_code=r[2],
                name=r[3],
                value=r[4],
                nominal=r[5]
            )
            for r in rows
        ]