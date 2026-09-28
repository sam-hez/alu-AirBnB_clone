#!/usr/bin/python3
"""Test the shared behavior of BaseModel."""
import unittest
from datetime import datetime
from unittest.mock import patch
from uuid import UUID

import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):
    """Check object creation, conversion, display, and saving."""

    def setUp(self):
        """Keep test objects separate from the shared storage."""
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        objects.start()
        self.addCleanup(objects.stop)

    def test_initial_values(self):
        """New objects have a UUID and datetime timestamps."""
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertEqual(UUID(model.id).version, 4)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertEqual(model.created_at, model.updated_at)
        self.assertIs(models.storage.all()["BaseModel." + model.id], model)

    def test_unique_ids(self):
        """Each new object receives a different ID."""
        self.assertNotEqual(BaseModel().id, BaseModel().id)

    def test_to_dict(self):
        """Conversion includes custom attributes and ISO timestamps."""
        model = BaseModel()
        model.name = "School"
        data = model.to_dict()
        self.assertEqual(data["id"], model.id)
        self.assertEqual(data["name"], "School")
        self.assertEqual(data["__class__"], "BaseModel")
        self.assertEqual(data["created_at"], model.created_at.isoformat())
        self.assertEqual(data["updated_at"], model.updated_at.isoformat())
        data["name"] = "Changed"
        self.assertEqual(model.name, "School")
        self.assertNotIn("__class__", model.__dict__)

    def test_restore_from_dictionary(self):
        """Restoring keeps values and does not register a new object."""
        model = BaseModel()
        model.name = "School"
        model.number = 7
        data = model.to_dict()
        models.storage.all().clear()
        restored = BaseModel(**data)
        self.assertEqual(restored.to_dict(), data)
        self.assertIsInstance(restored.created_at, datetime)
        self.assertIsInstance(restored.updated_at, datetime)
        self.assertNotIn("__class__", restored.__dict__)
        self.assertEqual(models.storage.all(), {})

    def test_string(self):
        """The display contains the class, ID, and object attributes."""
        model = BaseModel()
        expected = "[BaseModel] ({}) {}".format(model.id, model.__dict__)
        self.assertEqual(str(model), expected)

    def test_save(self):
        """Saving updates the modified time and calls storage."""
        model = BaseModel()
        created_at = model.created_at
        model.updated_at = datetime(2000, 1, 1)
        with patch.object(models.storage, "save") as save:
            model.save()
        self.assertGreater(model.updated_at, datetime(2000, 1, 1))
        self.assertEqual(model.created_at, created_at)
        save.assert_called_once_with()

    def test_positional_arguments(self):
        """Unused positional arguments do not prevent object creation."""
        model = BaseModel("unused", 12)
        self.assertIsInstance(model.id, str)


if __name__ == "__main__":
    unittest.main()
