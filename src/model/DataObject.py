from dataclasses import dataclass
from bson import ObjectId


@dataclass
class DataObject:
    _id: ObjectId
    name: str
