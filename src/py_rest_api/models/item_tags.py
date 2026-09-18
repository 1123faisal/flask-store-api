from sqlalchemy import Column, ForeignKey, Integer

from py_rest_api.db import db


class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
