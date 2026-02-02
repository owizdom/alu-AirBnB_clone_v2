#!/usr/bin/python3
"""State model"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """Return list of City instances with state_id == self.id"""
            from models import storage
            from models.city import City
            return [c for c in storage.all(City).values()
                    if c.state_id == self.id]
