from cryptography.fernet import Fernet
from crypto import AuthToken
from random import randint, randbytes


def encrypt(key, value):
    return Fernet(key)._encrypt_from_parts(value, 0, b"\xe1r\x11\x1e\xd4\xe1!U\xc9\xa2\xae\xc3\x8d\xf9\x01\xe9")


def decrypt(key, value):
    return Fernet(key).decrypt(value)


t = AuthToken("user", "pass")
salt = randint(0, 2**16)
iv = randbytes(16)

key = t.get_enc_key(salt)
enc = encrypt(key, b"aklsd")
print(enc)
dec = decrypt(key, enc)
print(dec)
