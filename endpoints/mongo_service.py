import certifi

ca = certifi.where()

from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://maciek:Key123@cluster0.ilfe3q4.mongodb.net/?retryWrites=true&w=majority"


def get_database():
    client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
    collection_name = client["sample_mflix"]["comments"]
    item_details = collection_name.find()
    for item in item_details:
        # This does not give a very readable output
        print(item)
    return client['users']


if __name__ == "__main__":
    dbname = get_database()
