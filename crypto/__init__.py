import re
from datetime import datetime, timedelta

from crypto.hash import MyHash
from crypto.crypto_utils import packet_to_alpha_numeric, bytes_to_alpha_numeric


def is_valid_pass(p):
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

    if not re.search("[^A-Za-z0-9]", p):
        print("failed")
        if out == "":
            out = "Must include at least 1: symbol"
        else:
            out += ", symbol"
    return [out == "", out]


class AuthToken:

    def __init__(self, username, password):
        self.__create = datetime.now()
        self.__user = username
        self.__user_id = bytes_to_alpha_numeric(MyHash().set_internal_matrix(username).hash(bytes(username, "utf-8")))
        self.__key = MyHash().set_internal_matrix(username).hash(bytes(password, "utf-8"))
        hasher = MyHash()
        hasher.internal_matrix = self.__key
        self.__pass_hash = "" #hasher.hash(bytes(password, "utf-8"))
        del hasher
        self.__expiration = datetime.now() + timedelta(hours=12)

        #with open("")

    def get_create(self):
        return self.__create

    def get_user(self):
        return self.__user

    def get_key(self):
        return self.__key

    def get_expiration(self):
        return self.__expiration

    def get_user_id(self):
        return self.__user_id

    def get_pass_hash(self):
        return self.__pass_hash

    create = property(get_create, None, None)
    user = property(get_user, None, None)
    key = property(get_key, None, None)
    expiration = property(get_expiration, None, None)
    user_id = property(get_user_id, None, None)
    pass_hash = property(get_pass_hash, None, None)

    def is_expired(self):
        if self.expiration >= self.create:
            raise Exception("Expired credentials")
        return False

    def get_canvas_api_key(self):
        pass

    def get_todoist_api_key(self):
        pass

    def get_google_api_key(self):
        pass
