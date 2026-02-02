#!/usr/bin/python3
"""Tests for BaseModel."""
import os
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel."""

    def tearDown(self):
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_base_model_creation(self):
        """Test BaseModel instance creation."""
        b = BaseModel()
        self.assertIsNotNone(b.id)
        self.assertIsNotNone(b.created_at)
        self.assertIsNotNone(b.updated_at)

    def test_base_model_to_dict(self):
        """Test BaseModel to_dict."""
        b = BaseModel()
        d = b.to_dict()
        self.assertIn("__class__", d)
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)

    def test_base_model_str(self):
        """Test BaseModel __str__."""
        b = BaseModel()
        s = str(b)
        self.assertIn("BaseModel", s)
        self.assertIn(b.id, s)

    def test_base_model_save(self):
        """Test BaseModel save."""
        b = BaseModel()
        old_updated = b.updated_at
        b.save()
        self.assertNotEqual(old_updated, b.updated_at)

    def test_base_model_init_kwargs(self):
        """Test BaseModel init with kwargs."""
        b = BaseModel(name="test")
        self.assertEqual(b.name, "test")
