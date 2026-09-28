#!/usr/bin/python3
"""Store model objects in a JSON file."""
import json


class FileStorage:
    """Manage objects in memory and save or reload them as JSON."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary of stored objects."""
        return self.__objects

    def new(self, obj):
        """Store an object using its class name and ID as the key."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Write all stored objects to the JSON file."""
        data = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def reload(self):
        """Restore stored objects if the JSON file exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel, "User": User, "Place": Place,
            "State": State, "City": City, "Amenity": Amenity,
            "Review": Review,
        }
        try:
            with open(self.__file_path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return
        for key, value in data.items():
            self.__objects[key] = classes[value["__class__"]](**value)
