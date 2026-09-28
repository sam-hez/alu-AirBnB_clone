import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def test_initial_values(self):
        model = BaseModel()

        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_unique_ids(self):
        self.assertNotEqual(BaseModel().id, BaseModel().id)


if __name__ == "__main__":
    unittest.main()