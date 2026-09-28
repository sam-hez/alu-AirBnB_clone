#!/usr/bin/python3
"""Test file storage with temporary files and isolated objects."""
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Check object registration and JSON persistence."""

    def setUp(self):
        """Use a fresh storage dictionary and a temporary file path."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = os.path.join(directory.name, "file.json")
        file_path = patch.object(FileStorage, "_FileStorage__file_path",
                                 self.path)
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        file_path.start()
        objects.start()
        self.addCleanup(file_path.stop)
        self.addCleanup(objects.stop)
        self.storage = FileStorage()

    def test_all(self):
        """An empty store returns its dictionary of objects."""
        self.assertEqual(self.storage.all(), {})
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Objects are indexed by class name and ID."""
        obj = BaseModel()
        self.storage.all().clear()
        self.storage.new(obj)
        self.assertEqual(self.storage.all(), {"BaseModel." + obj.id: obj})
        self.storage.new(obj)
        self.assertEqual(len(self.storage.all()), 1)

    def test_save(self):
        """Saving writes object dictionaries as valid JSON."""
        obj = BaseModel()
        obj.name = "Example"
        self.storage.save()
        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data, {"BaseModel." + obj.id: obj.to_dict()})

    def test_reload_all_models(self):
        """Every model is restored with its original type and values."""
        classes = (BaseModel, User, Place, State, City, Amenity, Review)
        expected = {}
        for model_class in classes:
            obj = model_class()
            obj.name = "Example"
            key = "{}.{}".format(model_class.__name__, obj.id)
            expected[key] = (model_class, obj.to_dict())
        self.storage.save()
        self.storage.all().clear()
        self.storage.reload()
        self.assertEqual(set(self.storage.all()), set(expected))
        for key, (model_class, data) in expected.items():
            with self.subTest(model=key):
                restored = self.storage.all()[key]
                self.assertIsInstance(restored, model_class)
                self.assertEqual(restored.to_dict(), data)

    def test_reload_missing_file(self):
        """A missing file leaves the existing objects unchanged."""
        obj = BaseModel()
        self.storage.reload()
        self.assertEqual(self.storage.all(), {"BaseModel." + obj.id: obj})

    def test_save_empty_store(self):
        """An empty store can be saved and loaded."""
        self.storage.save()
        with open(self.path, encoding="utf-8") as file:
            self.assertEqual(json.load(file), {})
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    def test_model_save_persists_changes(self):
        """Calling a model's save method writes its changed attributes."""
        obj = User()
        obj.email = "student@example.com"
        obj.save()
        self.storage.all().clear()
        self.storage.reload()
        restored = self.storage.all()["User." + obj.id]
        self.assertEqual(restored.email, "student@example.com")
        self.assertEqual(restored.updated_at, obj.updated_at)


if __name__ == "__main__":
    unittest.main()
