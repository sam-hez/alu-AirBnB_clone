#!/usr/bin/python3
"""Test the Place model and its default attributes."""
import unittest
from unittest.mock import patch

from models.base_model import BaseModel
from models.place import Place
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):
    """Check defaults and inherited model behavior."""

    def setUp(self):
        """Keep test instances separate from shared storage."""
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        objects.start()
        self.addCleanup(objects.stop)

    def test_defaults(self):
        """New instances have the expected default values and types."""
        obj = Place()
        self.assertIsInstance(obj, BaseModel)
        self.assertEqual(obj.city_id, '')
        self.assertIsInstance(obj.city_id, str)
        self.assertEqual(obj.user_id, '')
        self.assertIsInstance(obj.user_id, str)
        self.assertEqual(obj.name, '')
        self.assertIsInstance(obj.name, str)
        self.assertEqual(obj.description, '')
        self.assertIsInstance(obj.description, str)
        self.assertEqual(obj.number_rooms, 0)
        self.assertIsInstance(obj.number_rooms, int)
        self.assertEqual(obj.number_bathrooms, 0)
        self.assertIsInstance(obj.number_bathrooms, int)
        self.assertEqual(obj.max_guest, 0)
        self.assertIsInstance(obj.max_guest, int)
        self.assertEqual(obj.price_by_night, 0)
        self.assertIsInstance(obj.price_by_night, int)
        self.assertEqual(obj.latitude, 0.0)
        self.assertIsInstance(obj.latitude, float)
        self.assertEqual(obj.longitude, 0.0)
        self.assertIsInstance(obj.longitude, float)
        self.assertEqual(obj.amenity_ids, [])
        self.assertIsInstance(obj.amenity_ids, list)

    def test_dictionary_round_trip(self):
        """Custom attributes and model types survive reconstruction."""
        obj = Place()
        obj.name = "Example"
        data = obj.to_dict()
        self.assertEqual(data["__class__"], "Place")
        restored = Place(**data)
        self.assertEqual(restored.to_dict(), data)
        self.assertIsNot(restored, obj)


if __name__ == "__main__":
    unittest.main()
