import certifi
from pymongo import MongoClient

ca = certifi.where()
mongo_password = "Key123"
CONNECTION_STRING = "mongodb+srv://maciek:" + mongo_password + "@pyauth.9snukiq.mongodb.net/?retryWrites=true&w=majority"


def get_database():
    client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
    return client["PyAuth"]
    # return db['Users']


if __name__ == "__main__":
    dbname = get_database()


def get_user_by_email(email):
    return get_database()['Users'].find()
