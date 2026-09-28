#!/usr/bin/python3
"""Define the Review model."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review in the AirBnB clone."""

    place_id = ""
    user_id = ""
    text = ""
