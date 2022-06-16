from src.exceptions.NotFoundException import NotFoundException
from src.model.Folder import Folder
from src.model.User import User
import motor.motor_asyncio

mongo_password = "Key123"
CONNECTION_STRING = "mongodb+srv://maciek:" + mongo_password + "@pyauth.9snukiq.mongodb.net/?retryWrites=true&w=majority"


def get_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
    return client["PyAuth"]


async def get_user_by_name(name):
    query = {"name": name}
    user_dict = await get_database()["Users"].find_one(query)
    if user_dict is None:
        raise NotFoundException
    else:
        user = User(**user_dict)
        return user


async def add_new_user(user):
    user_dict = dict(_id=user._id,
                     name=user.name,
                     pass_hash=user.pass_hash,
                     main_folder=user.main_folder,
                     shared_folder=user.shared_folder)

    await get_database()["Users"].insert_one(user_dict)


async def add_folder_to_folder(folder_name, folder_id, parent_folder_id):
    query = {'_id': parent_folder_id}
    new_folder = {"_id": folder_id, "name": folder_name}
    options = {'$push': {'folders': new_folder}}
    await get_database()["Folders"].update_one(query, options)


async def add_file_to_folder(file_name, file_id, parent_folder_id):
    query = {'_id': parent_folder_id}
    new_file = {"_id": file_id, "name": file_name}
    options = {'$push': {'files': new_file}}
    await get_database()["Folders"].update_one(query, options)


async def add_new_folder(folder_name, folder_id, owner_id):
    folder = {"_id": folder_id,
              "name": folder_name,
              "folders": [],
              "files": [],
              "owners": [owner_id]}
    await get_database()["Folders"].insert_one(folder)


async def get_folder(folder_id):
    query = {"_id": folder_id}
    folder_dict = await get_database()["Folders"].find_one(query)
    folder = Folder(**folder_dict)
    return folder
