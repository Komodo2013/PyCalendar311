from kivy.logger import Logger
import json
import sqlite3 as sq

from data.encryptedDB import EncryptedDB


class UnauthorizedAccess(Exception):
    pass


class DB:
    user_db = False
    task_db = False

    def __init__(self):
        Logger.info(f"Starting Database")

    def get_user(self, user_id):
        if not self.user_db:
            return None
        for u in self.user_db:
            if u["user_id"] == user_id:
                return u

    def get_user_database(self, AuthToken):
        if not self.task_db:
            self.task_db = EncryptedDB(AuthToken)
        return self.task_db

    def start_user_db(self):
        if not self.user_db:
            with open("data/users.json", "a+"):
                pass

            with open("data/users.json", "r+") as users:
                json_file = users.read()
                if len(json_file) == 0:
                    self.user_db = []
                else:
                    self.user_db = json.loads(json_file)
        return self

    def start_database(self, AuthToken):
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

        if not self.user_db:
            return False

        for u in self.user_db:
            if u.user_id == user_id:
                return True
        return False

    def add_user(self, AuthToken):
        Logger.info("Writing new user entry")
        user = {
            "user_id": AuthToken.get_user_id(),
            "password": AuthToken.get_pass_hash(),
            "canvas_api_key": None,
            "todoist_api_key": None,
            "google_api_key": None
        }
        self.user_db.append(user)
        with open("data/users.json", "a+") as users:
            json.dump(user, users, ensure_ascii=True)
        return self

    def update_token(self, AuthToken):
        Logger.info("Updating user entry")
        user = {
            "user_id": AuthToken.get_user_id(),
            "password": AuthToken.get_pass_hash(),
            "canvas_api_key": AuthToken.get_canvas_api_key,
            "todoist_api_key": AuthToken.get_todoist_api_key,
            "google_api_key": AuthToken.get_google_api_key
        }

        for i in range(len(self.user_db)):
            if self.user_db[i]["user_id"] == user["user_id"]:
                self.user_db[i] = user

        with open("data/users.json", "r+") as users:
            for line in users:
                if user["user_id"] in line:
                    json.dump(user, users, ensure_ascii=True)


my_db = DB()
my_db.start_user_db()
