#!/usr/bin/python3
"""Create and load the shared file storage instance."""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
