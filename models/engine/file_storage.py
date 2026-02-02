#!/usr/bin/python3
"""FileStorage module"""
import json
import os

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes back"""
    __file_path = "file.json"
    __objects = {}

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def all(self, cls=None):
        """Return all objects, optionally filtered by class"""
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = FileStorage.classes.get(cls)
        if cls is None:
            return {}
        return {k: v for k, v in FileStorage.__objects.items()
                if isinstance(v, cls)}

    def new(self, obj):
        """Add new object to storage dictionary"""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize objects to JSON file"""
        obj_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize JSON file to objects"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        for key, obj_dict in data.items():
            class_name = obj_dict.get("__class__")
            cls = FileStorage.classes.get(class_name)
            if cls is None:
                continue
            FileStorage.__objects[key] = cls(**obj_dict)

    def delete(self, obj=None):
        """Delete obj from __objects if it exists"""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects.pop(key, None)
