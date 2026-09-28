#!/usr/bin/python3
"""Test the Review model and its default attributes."""
import unittest
from unittest.mock import patch

from models.base_model import BaseModel
from models.review import Review
from models.engine.file_storage import FileStorage


class TestReview(unittest.TestCase):
    """Check defaults and inherited model behavior."""

    def setUp(self):
        """Keep test instances separate from shared storage."""
        objects = patch.object(FileStorage, "_FileStorage__objects", {})
        objects.start()
        self.addCleanup(objects.stop)

    def test_defaults(self):
        """New instances have the expected default values and types."""
        obj = Review()
        self.assertIsInstance(obj, BaseModel)
        self.assertEqual(obj.place_id, '')
        self.assertIsInstance(obj.place_id, str)
        self.assertEqual(obj.user_id, '')
        self.assertIsInstance(obj.user_id, str)
        self.assertEqual(obj.text, '')
        self.assertIsInstance(obj.text, str)

    def test_dictionary_round_trip(self):
        """Custom attributes and model types survive reconstruction."""
        obj = Review()
        obj.name = "Example"
        data = obj.to_dict()
        self.assertEqual(data["__class__"], "Review")
        restored = Review(**data)
        self.assertEqual(restored.to_dict(), data)
        self.assertIsNot(restored, obj)


if __name__ == "__main__":
    unittest.main()
