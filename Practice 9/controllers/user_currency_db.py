from typing import List, Tuple

from utils.database import Database


class UserCurrencyDB:
    def __init__(self, db: Database):
        self.db = db

    def create(self, user_id: int, currency_id: int) -> int:
        """
        Создать подписку пользователя на валюту

        :param user_id: ID пользователя
        :param currency_id: ID валюты
        :return: ID записи с валютой
        """
        sql = "INSERT INTO user_currency(user_id, currency_id) VALUES (?, ?)"
        cur = self.db.get_connection().cursor()
        cur.execute(sql, (user_id, currency_id))
        self.db.get_connection().commit()
        return cur.lastrowid

    def read_user_currencies(self, user_id: int) -> List[Tuple[int, str, str, str, float, int]]:
        """
        Возвращает данные о валютах, на которые подписан пользователь.

        :param user_id: ID пользователя
        :return: список кортежей (id, num_code, char_code, name, value, nominal)
        """
        sql = """
              SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
              FROM user_currency uc
                       JOIN currency c ON uc.currency_id = c.id
              WHERE uc.user_id = ? \
              """
        rows = self.db.get_connection().execute(sql, (user_id,)).fetchall()
        return [
            (
                r['id'],
                r['num_code'],
                r['char_code'],
                r['name'],
                float(r['value']),
                r['nominal']
            )
            for r in rows
        ]