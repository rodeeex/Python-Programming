import sqlite3


class Database:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num_code TEXT NOT NULL,
                    char_code TEXT NOT NULL,
                    name TEXT NOT NULL,
                    value REAL,
                    nominal INTEGER NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user_currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    currency_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id),
                    FOREIGN KEY(currency_id) REFERENCES currency(id)
                )
            """)

    def get_connection(self) -> sqlite3.Connection:
        return self.conn

    def close(self):
        self.conn.close()