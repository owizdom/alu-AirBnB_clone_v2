#!/usr/bin/python3
"""Tests for FileStorage delete and all(cls)"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.state import State


class TestFileStorageDeleteAll(unittest.TestCase):
    def setUp(self):
        self.fs = FileStorage()
        try:
            os.remove("file.json")
        except OSError:
            pass
        self.fs.reload()

    def test_all_with_cls(self):
        s1 = State(name="California")
        self.fs.new(s1)
        self.fs.save()
        states = self.fs.all(State)
        self.assertIn(f"State.{s1.id}", states)

    def test_delete(self):
        s1 = State(name="California")
        self.fs.new(s1)
        self.fs.save()
        self.fs.delete(s1)
        states = self.fs.all(State)
        self.assertNotIn(f"State.{s1.id}", states)
