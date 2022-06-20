import os
import aiofiles
from src.utils import get_project_root, get_random_object_id
import src.endpoints.mongo_service as db_service


async def add_new_file(file_name, file_bytes, folder_id):
    file_id = get_random_object_id()
    file_path = os.path.join(get_project_root(), "res/files/"+str(file_id)+".txt")
    async with aiofiles.open(file_path, 'wb') as file:
        await file.write(file_bytes)
        await file.close()
    await db_service.add_file_to_folder(file_name, file_id, folder_id)


async def get_file(file_id, folder_id):
    file_path = os.path.join(get_project_root(), "res/files/" + str(file_id) + ".txt")
    folder = await db_service.get_folder(folder_id)
    for file in folder.files:
        if file["_id"] == file_id:
            return file_path, file["name"]

