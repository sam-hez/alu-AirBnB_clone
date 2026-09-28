#!/usr/bin/python3
"""Define the User model."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represent a user in the AirBnB clone."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
