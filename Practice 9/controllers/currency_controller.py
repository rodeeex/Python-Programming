from typing import List

from controllers.currency_db import CurrencyDB
from models.currency import Currency


class CurrencyController:
    def __init__(self, crud: CurrencyDB):
        self.crud = crud

    def list_currencies(self) -> List[Currency]:
        """
        Возвращает список всех валют

        :return: список Currency
        """
        return self.crud.read()

    def update_currency(self, char_code: str, value: float):
        """
        Обновляет курс валюты

        :param char_code: символьный код валюты
        :param value: новый курс
        """
        self.crud.update(char_code, value)

    def delete_currency(self, currency_id: int):
        """
        Удаляет валюту по ID

        :param currency_id: идентификатор валюты
        """
        self.crud.delete(currency_id)

    def create_currency(self, num_code: str, char_code: str, name: str, value: float, nominal: int) -> int:
        """
        Создаёт новую валюту.

        :param num_code: цифровой код валюты
        :param char_code: символьный код валюты
        :param name: название
        :param value: курс
        :param nominal: номинал
        :return: ID новой валюты
        """
        return self.crud.create(num_code, char_code, name, value, nominal)
