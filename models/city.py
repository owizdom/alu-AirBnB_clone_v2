#!/usr/bin/python3
"""City model"""
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """City class"""
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", backref="cities", cascade="all, delete")
