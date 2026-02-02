#!/usr/bin/python3
"""BaseModel module"""
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


def _utc_now():
    """Current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


class BaseModel:
    """Base class for all models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now)
    updated_at = Column(DateTime, nullable=False, default=_utc_now)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model"""
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                if k in ("created_at", "updated_at") and isinstance(v, str):
                    v = datetime.fromisoformat(v)
                object.__setattr__(self, k, v)
            if "id" not in self.__dict__:
                object.__setattr__(self, "id", str(uuid.uuid4()))
            if "created_at" not in self.__dict__:
                object.__setattr__(self, "created_at", _utc_now())
            if "updated_at" not in self.__dict__:
                object.__setattr__(self, "updated_at", _utc_now())
        else:
            object.__setattr__(self, "id", str(uuid.uuid4()))
            object.__setattr__(self, "created_at", _utc_now())
            object.__setattr__(self, "updated_at", _utc_now())

    def __str__(self):
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at and saves the instance to storage"""
        from models import storage
        self.updated_at = _utc_now()
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
