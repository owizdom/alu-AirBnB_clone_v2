#!/usr/bin/python3
"""BaseModel module"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """Base class for all models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model"""
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                if k in ("created_at", "updated_at") and isinstance(v, str):
                    setattr(self, k, datetime.fromisoformat(v))
                else:
                    setattr(self, k, v)
            if not getattr(self, "id", None):
                self.id = str(uuid.uuid4())
            if not getattr(self, "created_at", None):
                self.created_at = datetime.utcnow()
            if not getattr(self, "updated_at", None):
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at and saves the instance to storage"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        d = dict(self.__dict__)
        d["__class__"] = self.__class__.__name__
        if "created_at" in d and isinstance(d["created_at"], datetime):
            d["created_at"] = d["created_at"].isoformat()
        if "updated_at" in d and isinstance(d["updated_at"], datetime):
            d["updated_at"] = d["updated_at"].isoformat()
        d.pop("_sa_instance_state", None)
        return d

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)
