from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship

from py_rest_api.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=True)
    items = Relationship("ItemModel", back_populates="store", lazy="dynamic")
    tags = Relationship("TagModel", back_populates="store", lazy="dynamic")
