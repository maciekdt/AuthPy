from dataclasses import dataclass
from bson import ObjectId


@dataclass
class User:
    _id: ObjectId
    name: str
    pass_hash: bytes
    main_folder: ObjectId
    shared_folder: ObjectId
