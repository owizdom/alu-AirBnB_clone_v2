#!/usr/bin/python3
"""Amenity model"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Amenity class"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
            "Place", secondary=place_amenity, viewonly=False,
            back_populates="amenities")
