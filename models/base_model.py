#!/usr/bin/python3
"""Define the shared attributes and methods for all models."""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Give each object an ID, timestamps, and dictionary conversion."""

    def __init__(self, *args, **kwargs):
        """Create a new object or restore one from a dictionary."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Return the class name, ID, and attributes of the object."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update the timestamp and save objects to storage."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return attributes with a class name and ISO timestamps."""
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result
