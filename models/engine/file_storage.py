import json
forom models.base_model import BaseModal

class FileStorage:
    __file__path = "file.json"
    __objects = {}

    def all(self):

        return self.__objects
    
    def new(self, obj):

        key = f"{obj}"