import sqlite3 as sq

def get_user_database(user):
    return ""


def worker(task, cursor):
    result = cursor.execute(task)
    return result


class DB:
    user_db = False
    user_db_cursor = False
    task_db = False
    task_db_cursor = False

    def start_user_db(self):
        if not self.user_db:
            self.user_db = sq.connect("data/users.db")
            self.user_db_cursor = self.user_db.cursor()

        self.user_db_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            pass_hash BLOB NOT NULL,
            enc_canvas_key BLOB,
            enc_todoist_key BLOB,
            enc_google_key BLOB
        );""")
        return self

    def start_database(self, user):
        if not self.task_db:
            self.task_db = sq.connect(get_user_database(user))
            self.task_db_cursor = self.task_db.cursor()

        return self

    def user_exists(self, user_id):
        if not self.user_db:
            raise Exception("Database not initialized")

        worker("""
                """, self.user_db_cursor)

    def add_user(self, token):
        if not self.user_db:
            raise Exception("Database not initialized")

        worker(f"""INSERT INTO users (user_hash, pass_hash, enc_canvas_key, enc_todoist_key, enc_google_key)
         Values({token}
        )
        """, self.user_db_cursor)

        return self


my_db = DB()
my_db.start_user_db()
