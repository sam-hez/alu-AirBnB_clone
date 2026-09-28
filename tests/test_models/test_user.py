#!/usr/bin/python3
"""Test the User model and its default attributes."""
import unittest
from unittest.mock import patch

from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    """Check defaults and inherited model behavior."""

    def setUp(self):
        """Keep test instances separate from shared storage."""
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        objects.start()
        self.addCleanup(objects.stop)

    def test_defaults(self):
        """New instances have the expected default values and types."""
        obj = User()
        self.assertIsInstance(obj, BaseModel)
        self.assertEqual(obj.email, '')
        self.assertIsInstance(obj.email, str)
        self.assertEqual(obj.password, '')
        self.assertIsInstance(obj.password, str)
        self.assertEqual(obj.first_name, '')
        self.assertIsInstance(obj.first_name, str)
        self.assertEqual(obj.last_name, '')
        self.assertIsInstance(obj.last_name, str)

    def test_dictionary_round_trip(self):
        """Custom attributes and model types survive reconstruction."""
        obj = User()
        obj.name = "Example"
        data = obj.to_dict()
        self.assertEqual(data["__class__"], "User")
        restored = User(**data)
        self.assertEqual(restored.to_dict(), data)
        self.assertIsNot(restored, obj)


if __name__ == "__main__":
    unittest.main()
