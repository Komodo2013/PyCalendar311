import base64
import re
from datetime import datetime, timedelta

import data
from crypto.hash import MyHash
from crypto.crypto_utils import packet_to_alpha_numeric, bytes_to_alpha_numeric, packet_to_bytes, create_packets
from kivy.logger import Logger


def is_valid_pass(p):
    """
    out = ""

    if not re.search("[A-Z]", p) or not re.search("[a-z]", p):
        out = "Must include at least 1: Upper and Lower case letters"
    elif not re.search("[A-Z]", p):
        out = "Must include at least 1: Upper case letter"
    elif not re.search("[a-z]", p):
        out = "Must include at least 1: Lower case letter"

    if not re.search("[0-9]", p):
        if out == "":
            out = "Must include at least 1: number"
        else:
            out += ", number"
    """
    """
    if not re.search("[^A-Za-z0-9]", p):
        print("failed")
        if out == "":
            out = "Must include at least 1: symbol"
        else:
            out += ", symbol"
    """
    # return [out == "", out]
    return True


class AuthToken:

    def __init__(self, username, password):
        Logger.info(f"Creating AuthToken for {username}")

        self.__create = datetime.now()
        self.__user = username
        self.__user_id = base64.b64encode(
            MyHash().set_internal_matrix(username).hash(bytes(username, "utf-8"))).decode('ascii')
        print(self.__user_id)
        hasher = MyHash().set_internal_matrix(username)
        hasher.internal_matrix = hasher.hash_packs(create_packets(bytes(password, "utf-8")), iterations=10)
        self.__key = packet_to_bytes(hasher.internal_matrix)
        self.__pass_hash = base64.b64encode(hasher.hash(bytes(password, "utf-8"))).decode('ascii')
        del hasher
        self.__expiration = datetime.now() + timedelta(hours=3)

        self.__canvas_api_key = ""
        self.__todoist_api_key = ""
        self.__google_api_key = ""

    def get_enc_key(self):
        hasher = MyHash()
        hasher.internal_matrix = self.__key


    def get_create(self):
        return self.__create

    def get_user(self):
        return self.__user

    def get_expiration(self):
        return self.__expiration

    def get_user_id(self):
        return self.__user_id

    def get_pass_hash(self):
        return self.__pass_hash

    def is_expired(self):
        if self.expiration <= datetime.now():
            return True
        return False

    def get_canvas_api_key(self):
        if self.is_valid():
            return self.__canvas_api_key
        else:
            return None

    def get_todoist_api_key(self):
        if self.is_valid():
            return self.__todoist_api_key
        else:
            return None

    def get_google_api_key(self):
        if self.is_valid():
            return self.__google_api_key
        else:
            return None

    def set_canvas_api_key(self, key):
        if self.is_valid():
            self.__canvas_api_key = key
            return self
        else:
            return None

    def set_todoist_api_key(self, key):
        if self.is_valid():
            self.__todoist_api_key = key
            return self
        else:
            return None

    def set_google_api_key(self, key):
        if self.is_valid():
            self.__google_api_key = key
            return self
        else:
            return None

    def is_valid(self):
        print(data.my_db.get_user(self.__user_id), not self.is_expired())
        return data.my_db.get_user(self.__user_id) is not None and not self.is_expired()

    create = property(get_create, None, None)
    user = property(get_user, None, None)
    expiration = property(get_expiration, None, None)
    user_id = property(get_user_id, None, None)
    pass_hash = property(get_pass_hash, None, None)

    canvas_api_key = property(get_canvas_api_key, set_canvas_api_key, None)
    todoist_api_key = property(get_todoist_api_key, set_todoist_api_key, None)
    google_api_key = property(get_google_api_key, set_google_api_key, None)


