from endpoints.NotFoundException import NotFoundException
from model.User import User
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
        user_dict["_id"] = str(user_dict["_id"])
        user = User(**user_dict)
        return user


async def add_new_user(name, password):
    user_dict = {"name": name, "password": password}
    await get_database()["Users"].insert_one(user_dict)
