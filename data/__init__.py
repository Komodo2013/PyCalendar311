import sqlite3 as sq
import time


def user_exists(username):
    return None


class DB:
    connections = False
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return super().__init__(None)

    def connect(self):
        if not self.connections:
            self.user_db = sq.connect("users.db")
            self.classes_db = sq.connect("users.db")
            self.assignments_db = sq.connect("users.db")
            self.tasks_db = sq.connect("users.db")
            self.user_db = sq.connect("users.db")
