from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_rest_api.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(80), unique=True)

    items = relationship("ItemModel", back_populates="store", lazy="dynamic")
    tags = relationship("TagModel", back_populates="store", lazy="dynamic")
