import sqlite3
import time


def user_exists(username):
    return None


class DB:
    instance = None
    time = None

    def __init__(self):
        self.time = time.time()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return super().__init__(None)

import sys

print(sys.version)
