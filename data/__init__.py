from kivy.logger import Logger
import sqlite3 as sq


class UnauthorizedAccess(Exception):
    pass


class DB:
    user_db = False
    task_db = False

    def __init__(self):
        Logger.info(f"Starting Database")

    def get_user(self, user_id):
        cur = self.get_user_database().cursor()
        r = cur.execute(f"select * from Users where user_id=?", (user_id, ))
        return r.fetchone()

    def get_task_database(self, AuthToken):
        if not self.task_db:
            self.start_task_db(AuthToken)
        return self.task_db

    def get_user_database(self):
        if not self.user_db:
            self.start_user_db()
        return self.user_db

    def start_user_db(self):
        if not self.user_db:
            with open("data/users.db", "a+"):
                pass

            try:
                self.user_db = sq.connect("data/users.db")
                cur = self.user_db.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS Users (user_id TEXT PRIMARY KEY, password TEXT, "
                            "canvas_api_key TEXT, todoist_api_key TEXT, google_api_key TEXT);")
                self.user_db.commit()
            except sq.Error as e:
                Logger.error(e)
                raise e
        return self

    def start_task_db(self, AuthToken):
        if not self.task_db:
            Logger.info("Connecting to task_db")
            if not AuthToken.is_valid():
                raise UnauthorizedAccess
            # Create database file if it doesn't exist
            with open(f"data/{AuthToken.user_id[-10:]}.db", "w+"):
                pass

            try:
                self.task_db = sq.connect(f"data/{AuthToken.user_id[-10:]}.db")
            except sq.Error as e:
                Logger.error(e)
                raise e

        return self

    def user_exists(self, user_id):
        Logger.info("Finding user")
        print(self.get_user(user_id))
        if self.get_user(user_id):
            return True
        return False

    def add_user(self, AuthToken):
        Logger.info("Writing new user entry")
        user = (
            AuthToken.get_user_id(),
            AuthToken.get_pass_hash()
        )
        if not self.user_exists(user[0]):
            cur = self.get_user_database().cursor()
            cur.execute("insert into Users (user_id, password) values (?, ?)", user)
            self.get_user_database().commit()

    def update_token(self, AuthToken):
        Logger.info("Updating user entry")
        user = (
            AuthToken.get_user_id(),
            AuthToken.get_pass_hash(),
            AuthToken.get_canvas_api_key(),
            AuthToken.get_todoist_api_key(),
            AuthToken.get_google_api_key(),
            AuthToken.get_user_id()
        )

        if self.user_exists(user[0]):
            cur = self.get_user_database().cursor()
            cur.execute("update Users set user_id=?, password=?, canvas_api_key=?, todoist_api_key=?, "
                        "google_api_key=? where user_id=?", user)
            self.get_user_database().commit()


my_db = DB()
my_db.start_user_db()
