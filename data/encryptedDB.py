from kivy.logger import Logger
import sqlite3 as sq

special = "§"


class EncryptedDB:
    def __init__(self, AuthToken):
        # Create database file if it doesn't exist
        with open(f"data/{AuthToken.user_id[-10:]}.db", "w+"):
            pass

        try:
            self.connection = sq.connect(f"data/{AuthToken.user_id[-10:]}.db")
        except sq.Error as e:
            Logger.error(e)
            raise e

    def create_table(self, table_string):
        with self.connection.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_string};")
            self.connection.commit()

