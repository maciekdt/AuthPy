import os
import uuid
from src.utils import get_project_root


def add_new_file(file_name, file_bytes):
    file_id_name = str(uuid.uuid4()) + ".txt"
    file_path = os.path.join(get_project_root(), "res/files/"+file_id_name)
    file = open(file_path, "wb")
    file.write(file_bytes)
    file.close()
    return file_id_name


def get_file(file_id_name):
    file_path = os.path.join(get_project_root(), "res/files/"+file_id_name)
    file = open(file_path, "rb")
    result = file.read()
    file.close()
    return result
