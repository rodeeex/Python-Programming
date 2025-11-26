from models.currency import Currency
from typing import List
from utils.database import Database


class CurrencyRatesCRUD:
    def __init__(self, db: Database):
        self.db = db

    def create(self, num_code: str, char_code: str, name: str, value: float, nominal: int) -> int:
        """
        Создаёт новую валюту в БД

        :param num_code: цифровой код валюты
        :param char_code: символьный код валюты
        :param name: название валюты
        :param value: курс к рублю
        :param nominal: номинал, т.е. за сколько единиц указан курс
        :return: ID созданной записи
        """
        sql = """
              INSERT INTO currency(num_code, char_code, name, value, nominal)
              VALUES (?, ?, ?, ?, ?) \
              """
        cur = self.db.get_connection().cursor()
        cur.execute(sql, (num_code, char_code, name, value, nominal))
        self.db.get_connection().commit()
        return cur.lastrowid

    def read(self) -> List[Currency]:
        """
        Читает все валюты из БД

        :return: список объектов Currency
        """
        sql = "SELECT * FROM currency"
        cur = self.db.get_connection().cursor()
        rows = cur.execute(sql).fetchall()
        return [
            Currency(
                id_=row['id'],
                num_code=row['num_code'],
                char_code=row['char_code'],
                name=row['name'],
                value=row['value'],
                nominal=row['nominal']
            )
            for row in rows
        ]

    def update(self, char_code: str, value: float):
        """
        Обновляет курс валюты по символьному коду

        :param char_code: код валюты
        :param value: новый курс
        """
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        cur = self.db.get_connection().cursor()
        cur.execute(sql, (value, char_code))
        self.db.get_connection().commit()

    def delete(self, currency_id: int):
        """
        Удаляет валюту по ID

        :param currency_id: идентификатор валюты
        """
        sql = "DELETE FROM currency WHERE id = ?"
        cur = self.db.get_connection().cursor()
        cur.execute(sql, (currency_id,))
        self.db.get_connection().commit()
