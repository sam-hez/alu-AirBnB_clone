#!/usr/bin/python3
"""Test the City model and its default attributes."""
import unittest
from unittest.mock import patch

from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage


class TestCity(unittest.TestCase):
    """Check defaults and inherited model behavior."""

    def setUp(self):
        """Keep test instances separate from shared storage."""
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        objects.start()
        self.addCleanup(objects.stop)

    def test_defaults(self):
        """New instances have the expected default values and types."""
        obj = City()
        self.assertIsInstance(obj, BaseModel)
        self.assertEqual(obj.state_id, '')
        self.assertIsInstance(obj.state_id, str)
        self.assertEqual(obj.name, '')
        self.assertIsInstance(obj.name, str)

    def test_dictionary_round_trip(self):
        """Custom attributes and model types survive reconstruction."""
        obj = City()
        obj.name = "Example"
        data = obj.to_dict()
        self.assertEqual(data["__class__"], "City")
        restored = City(**data)
        self.assertEqual(restored.to_dict(), data)
        self.assertIsNot(restored, obj)


if __name__ == "__main__":
    unittest.main()
