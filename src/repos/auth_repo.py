import datetime
import jwt
from bson import ObjectId

import src.endpoints.mongo_service as db_service
import hashlib
import os
import aiofiles
from src.exceptions.NotFoundException import NotFoundException
from src.exceptions.UnauthorizedException import UnauthorizedException
from src.model.User import User
from src.utils import get_project_root, get_random_object_id

data_source = db_service
HASH_ITERATIONS = 100000
SALT_LEN = 32


async def login(name, password):
    try:
        user = await data_source.get_user_by_name(name)
        if verify_pass(password, user.pass_hash):
            token = await get_token_for_user(user.name, user._id)
            return token, user
        else:
            raise UnauthorizedException
    except NotFoundException:
        raise UnauthorizedException


async def register(name, password):
    pass_hash = encode_pass(password)
    user_id = get_random_object_id()
    main_folder_id = get_random_object_id()
    shared_folder_id = get_random_object_id()

    user = User(user_id, name, pass_hash, main_folder_id, shared_folder_id)
    await data_source.add_new_user(user)

    await data_source.add_new_folder("My files", main_folder_id, [user_id])
    await data_source.add_new_folder("Shared files", shared_folder_id, [user_id])


def encode_pass(password):
    salt = os.urandom(SALT_LEN)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    storage = salt + key
    return storage


def verify_pass(password_to_check, hash_from_storage):
    salt_from_storage = hash_from_storage[:SALT_LEN]
    key_from_storage = hash_from_storage[SALT_LEN:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_to_check.encode('utf-8'),
        salt_from_storage,
        HASH_ITERATIONS
    )
    return new_key == key_from_storage


async def get_token_for_user(name, user_id):
    page_path = os.path.join(get_project_root(), 'res/rsa_keys/private.key')
    async with aiofiles.open(page_path, 'rb') as file:
        private_key = await file.read()
        expire_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=3600)
        token = jwt.encode({"user": name, "user_id": str(user_id),  "exp": expire_time}, private_key, algorithm="RS256")
        return token


async def verify_token(token):
    page_path = os.path.join(get_project_root(), 'res/rsa_keys/public.key')
    async with aiofiles.open(page_path, 'rb') as file:
        private_key = await file.read()
        try:
            decoded = jwt.decode(token, private_key, algorithms=["RS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException
        except jwt.InvalidTokenError:
            raise UnauthorizedException


async def check_owner(request, folder_id):
    folder = await data_source.get_folder(ObjectId(folder_id))
    if request.ctx.user_id in folder.owners:
        return True
    else:
        raise UnauthorizedException
