from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_rest_api.db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(80), unique=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))

    store: Mapped["StoreModel"] = relationship(back_populates="tags")
    items: Mapped[list["ItemModel"]] = relationship(
        back_populates="tags", secondary="items_tags"
    )
