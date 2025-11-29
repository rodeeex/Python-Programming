from typing import List, Tuple
from models.user import User
from utils.database import Database


class UserDB:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str) -> int:
        sql = "INSERT INTO user(name) VALUES (?)"
        cur = self.db.get_connection().cursor()
        cur.execute(sql, (name,))
        self.db.get_connection().commit()
        return cur.lastrowid

    def read_all(self) -> List[User]:
        sql = "SELECT * FROM user"
        rows = self.db.get_connection().execute(sql).fetchall()
        return [User(row['id'], row['name']) for row in rows]

    def read_by_id(self, user_id: int) -> User | None:
        sql = "SELECT * FROM user WHERE id = ?"
        row = self.db.get_connection().execute(sql, (user_id,)).fetchone()
        return User(row['id'], row['name']) if row else None