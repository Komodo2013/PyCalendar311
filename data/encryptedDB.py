from random import randint

from kivy.logger import Logger
import sqlite3 as sq
from cryptography.fernet import Fernet


def encrypt(key, value):
    return Fernet(key)._encrypt_from_parts(value, 0, b"\xe1r\x11\x1e\xd4\xe1!U\xc9\xa2\xae\xc3\x8d\xf9\x01\xe9")


def decrypt(key, value):
    return Fernet(key).decrypt(value)


class UnauthorizedAccess(Exception):
    pass


"""

THIS IS NO LONGER USED

I began working on an encrypted database, but realized that this is overkill for the data that is being saved
Since the database is local, the chance of online attacks are slim, with the greatest threat being an individual gaining
access to your phone physically. If they have access to your phone/computer, then they likely already have your calendar
Assignment grades would then be unprotected, although there isn't much an attacker can do with this

The api keys are encrypted using my elliptical curve cryptography module, which is effectively the only important 
information we would need to protect. According to my tests, my cryptography module would take too long to attack to
make an attack for API keys reasonable.

"""


class EncryptedDB:
    def __init__(self, AuthToken):
        if not AuthToken.is_valid():
            raise UnauthorizedAccess
        # Create database file if it doesn't exist
        with open(f"data/{AuthToken.user_id[-10:]}.db", "w+"):
            pass

        try:
            self.connection = sq.connect(f"data/{AuthToken.user_id[-10:]}.db")
            self.AuthToken = AuthToken
        except sq.Error as e:
            Logger.error(e)
            raise e

    def create_table(self, table_name, column_list, data_type_list):
        columns = ""
        if len(column_list) != len(data_type_list):
            raise

        for i in range(len(column_list)):
            columns += ("" if i == 0 else ", ") + f"{column_list[i]} {data_type_list[i]}"

        with self.connection.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
            self.connection.commit()

    def query_table(self, table_string):
        with self.connection.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_string};")
            self.connection.commit()

    def update_records(self, table_string):
        with self.connection.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_string};")
            self.connection.commit()

    def remove_records(self, AuthToken, table_name, condition):
        if AuthToken.user_id != self.AuthToken.user_id or self.AuthToken.is_expired():
            raise UnauthorizedAccess

        with self.connection.cursor() as cur:
            cur.execute(f"DELETE FROM {table_name} WHERE {condition};")
            self.connection.commit()

    def insert_records(self, AuthToken, table_name, columns_list, values_list):
        if len(columns_list) != len(values_list):
            raise sq.OperationalError

        if AuthToken.user_id != self.AuthToken.user_id or self.AuthToken.is_expired():
            raise UnauthorizedAccess

        salt = randint(0, 2**16)
        columns, values = "", ""
        key = AuthToken.get_enc_key(salt)

        for i in range(len(columns_list)):
            columns += columns_list[i] if i == 0 else f", {columns_list[i]}"
            values += encrypt(key, values_list[i]) if i == 0 else f", {encrypt(key, values_list[i])}"

        with self.connection.cursor() as cur:
            cur.execute(f"INSERT INTO {table_name} (salt, {columns}) VALUES ({salt}, {values});")
            self.connection.commit()
