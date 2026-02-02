#!/usr/bin/python3
"""Tests for DBStorage engine."""
import os
import unittest


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage tests")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage."""

    def test_db_storage_all(self):
        """Test DBStorage all() returns dict."""
        from models import storage
        objs = storage.all()
        self.assertIsInstance(objs, dict)

    def test_db_storage_all_with_cls(self):
        """Test DBStorage all(State) returns dict."""
        from models import storage
        from models.state import State
        objs = storage.all(State)
        self.assertIsInstance(objs, dict)

    def test_db_storage_new_save(self):
        """Test DBStorage new() and save()."""
        from models import storage
        from models.state import State
        s = State(name="TestState")
        storage.new(s)
        storage.save()
        objs = storage.all(State)
        self.assertIn("State.{}".format(s.id), objs)
        storage.delete(s)
        storage.save()
