import endpoints.mongo_service as db_service
import hashlib
import os

data_source = db_service


async def login(name, password):
    user = await data_source.get_user_by_name(name)
    if user is not None and user.password == password:
        return True
    else:
        return False


async def register(name, password):
    await data_source.add_new_user(name, password)


def encode_pass(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    storage = salt + key
    return storage


def verify_pass(password_to_check, hash_from_storage):
    salt_from_storage = hash_from_storage[:32]
    key_from_storage = hash_from_storage[32:]

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_to_check.encode('utf-8'),  # Convert the password to bytes
        salt_from_storage,
        100000
    )
    return new_key == key_from_storage
