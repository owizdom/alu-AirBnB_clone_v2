#!/usr/bin/python3
"""Place model"""
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False),
)


class _PlaceAmenityList:
    """Proxy list so place.amenities.append(amenity) adds amenity.id to place.amenity_ids."""

    def __init__(self, place):
        self._place = place

    def __iter__(self):
        from models import storage
        from models.amenity import Amenity
        for a in storage.all(Amenity).values():
            if a.id in self._place.amenity_ids:
                yield a

    def append(self, amenity):
        from models.amenity import Amenity
        if isinstance(amenity, Amenity) and amenity.id not in self._place.amenity_ids:
            self._place.amenity_ids.append(amenity.id)


class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place", cascade="all, delete")
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False, back_populates="place_amenities")
    else:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.amenity_ids = list(getattr(self, "amenity_ids", []))

        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            return [r for r in storage.all(Review).values() if r.place_id == self.id]

        @property
        def amenities(self):
            return _PlaceAmenityList(self)

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
