from dataclasses import dataclass
from bson import ObjectId


@dataclass
class Folder:
    _id: ObjectId
    name: str
    folders: []
    files: []
    owners: []
