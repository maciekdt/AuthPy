import datetime
import jwt
import src.endpoints.mongo_service as db_service
import hashlib
import os
import aiofiles
import asyncio

from src.exceptions import NotFoundException, UnauthorizedException
from src.utils import get_project_root

data_source = db_service


async def login(name, password):
    try:
        user = await data_source.get_user_by_name(name)
        if verify_pass(password, user.pass_hash):
            token = await get_token_for_name(name)
            return token
        else:
            raise UnauthorizedException
    except NotFoundException:
        raise UnauthorizedException


async def register(name, password):
    pass_hash = encode_pass(password)
    await data_source.add_new_user(name, pass_hash)


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
        password_to_check.encode('utf-8'),
        salt_from_storage,
        100000
    )
    return new_key == key_from_storage


async def get_token_for_name(name):
    page_path = os.path.join(get_project_root(), 'res/rsa_keys/private.key')
    async with aiofiles.open(page_path, 'rb') as file:
        private_key = await file.read()
        expire_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=10)
        token = jwt.encode({"user": name, "exp": expire_time}, private_key, algorithm="RS256")
        return token


async def verify_token(token):
    page_path = os.path.join(get_project_root(), 'res/rsa_keys/public.key')
    async with aiofiles.open(page_path, 'rb') as file:
        private_key = await file.read()
        try:
            decoded = jwt.decode(token, private_key, algorithms=["RS256"])
            return decoded["user"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
