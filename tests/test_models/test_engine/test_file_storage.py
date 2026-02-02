#!/usr/bin/python3
"""Tests for FileStorage engine."""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State


class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage."""

    def setUp(self):
        self.fs = FileStorage()
        try:
            os.remove("file.json")
        except OSError:
            pass
        self.fs.reload()

    def tearDown(self):
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_all_returns_dict(self):
        """Test all() returns a dict."""
        objs = self.fs.all()
        self.assertIsInstance(objs, dict)

    def test_new_and_save(self):
        """Test new() and save()."""
        b = BaseModel()
        self.fs.new(b)
        self.fs.save()
        objs = self.fs.all()
        self.assertIn("BaseModel.{}".format(b.id), objs)

    def test_reload(self):
        """Test reload()."""
        b = BaseModel()
        self.fs.new(b)
        self.fs.save()
        self.fs.reload()
        objs = self.fs.all()
        self.assertIn("BaseModel.{}".format(b.id), objs)

    def test_all_with_cls(self):
        """Test all(State) returns only State objects."""
        s = State(name="CA")
        self.fs.new(s)
        self.fs.save()
        states = self.fs.all(State)
        self.assertIn("State.{}".format(s.id), states)

    def test_delete(self):
        """Test delete()."""
        s = State(name="CA")
        self.fs.new(s)
        self.fs.save()
        self.fs.delete(s)
        states = self.fs.all(State)
        self.assertNotIn("State.{}".format(s.id), states)
