#!/usr/bin/python3
"""Tests for console parameterized create (FileStorage only)"""
import os
import unittest
from unittest.mock import patch
from io import StringIO

from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage-only create param tests")
class TestConsoleCreateParams(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_create_state_with_name(self):
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            obj_id = f.getvalue().strip()
        self.assertTrue(obj_id)
        objs = storage.all(State)
        self.assertTrue(any(o.id == obj_id and o.name == "California" for o in objs.values()))

    def test_create_place_types(self):
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 latitude=37.5')
            obj_id = f.getvalue().strip()
        created = [o for o in storage.all(Place).values() if o.id == obj_id][0]
        self.assertEqual(created.name, "My little house")
        self.assertEqual(created.number_rooms, 4)
        self.assertAlmostEqual(created.latitude, 37.5)
