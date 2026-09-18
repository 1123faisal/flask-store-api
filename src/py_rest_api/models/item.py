from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from py_rest_api.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    price = Column(Float(precision=2), unique=False, nullable=False)
    desc = Column(String)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=False, nullable=False)

    store = Relationship("StoreModel", back_populates="items")
    tags = Relationship("TagModel", back_populates="items", secondary="items_tags")
