from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from py_rest_api.db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)

    store = Relationship("StoreModel", back_populates="tags")
    items = Relationship("ItemModel", back_populates="tags", secondary="items_tags")
