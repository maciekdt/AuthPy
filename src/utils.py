import os
from pathlib import Path
from bson import ObjectId


def get_project_root() -> Path:
    return Path(__file__).parent


def get_random_object_id():
    string_size = 12
    return ObjectId(os.urandom(string_size).hex())
