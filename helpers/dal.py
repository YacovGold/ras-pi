import sqlite3


class Dal:
    def __init__(self, key_prefix: str, db_path: str):
        self.db_path = db_path
        self.key_prefix = key_prefix
        self.conn = sqlite3.connect(self.db_path)
        self._setup_database()

    def __del__(self):
        self.conn.close()

    def get_val(self, key: str, default: str):
        full_key = f"{self.key_prefix }: {key}"
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM data WHERE key=?", (full_key,))
            result = cursor.fetchone()
            return result[0] if result else default

    def set_val(self, key: str, val: str):
        full_key = f"{self.key_prefix }: {key}"
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO data (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (full_key, val))
            self.conn.commit()

    def _setup_database(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            self.conn.commit()
