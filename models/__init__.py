#!/usr/bin/python3
"""Initializes the models package"""
import os

storage = None

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage  # noqa: E402
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage  # noqa: E402
    storage = FileStorage()

storage.reload()
