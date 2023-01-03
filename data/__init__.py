import sqlite3
import sqlite3 as sq

import crypto
from kivy.logger import Logger


def get_user_database(user):
    return f"data/{user}"


class DB:
    user_db = False
    user_db_cursor = False
    task_db = False
    task_db_cursor = False

    def __init__(self):
        Logger.info(f"Starting Database")


    def start_user_db(self):
        if not self.user_db:
            Logger.info("Connecting to user_db")
            self.user_db = sq.connect("data/users.db")
            self.user_db_cursor = self.user_db.cursor()

        self.user_db_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            pass_hash BLOB NOT NULL,
            enc_canvas_key BLOB,
            enc_todoist_key BLOB,
            enc_google_key BLOB
        );""")
        self.user_db.commit()
        return self

    def start_database(self, AuthToken):
        if not self.task_db:
            Logger.info("Connecting to task_db")
            self.task_db = sq.connect(get_user_database(AuthToken.user_id))
            self.task_db_cursor = self.task_db.cursor()

        return self

    def user_exists(self, user_id):
        Logger.info("Finding user")

        if not self.user_db:
            raise Exception("Database not initialized")

        try:
            self.user_db_cursor.execute(f"""Select * from users where user_id = '{user_id}'""")
            return len(self.user_db_cursor.fetchall()) > 0
        except sqlite3.OperationalError:
            return False

    def add_user(self, token):
        Logger.info("Connecting to task_db")

        if not self.user_db:
            raise Exception("Database not initialized")
        self.user_db_cursor.execute(f"""insert into users (user_id, pass_hash) Values (?, ?)""",
                                    [token.user_id, memoryview(token.pass_hash)])
        self.user_db.commit()
        return self


my_db = DB()
my_db.start_user_db()
