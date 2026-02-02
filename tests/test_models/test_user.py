#!/usr/bin/python3
"""Tests for User model."""
import os
import unittest
from models.user import User


class TestUser(unittest.TestCase):
    """Tests for User."""

    def tearDown(self):
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_user_creation(self):
        """Test User instance creation."""
        u = User(email="a@b.com", password="pwd")
        self.assertIsNotNone(u.id)
        self.assertEqual(u.email, "a@b.com")
        self.assertEqual(u.password, "pwd")

    def test_user_attributes(self):
        """Test User optional attributes."""
        u = User(
            email="a@b.com", password="pwd",
            first_name="John", last_name="Doe"
        )
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")

    def test_user_to_dict(self):
        """Test User to_dict."""
        u = User(email="a@b.com", password="pwd")
        d = u.to_dict()
        self.assertEqual(d["__class__"], "User")
        self.assertIn("email", d)
        self.assertIn("password", d)
