import uuid
import datetime

class BaseModel:

    def __init__(self, *args, **kwargs):

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, datetime.datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            storage.new(self)

    def save(self):
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        # Returns a dictiionary representation of the instance
        my_obj_dict = self.__dict__.copy()
        my_obj_dict["__class__"] = self.__class__.__name__
        my_obj_dict["created_at"] = self.created_at.isoformat()
        my_obj_dict["updated_at"] = self.updated_at.isoformat()
        return my_obj_dict

    