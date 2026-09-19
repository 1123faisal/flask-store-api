from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_rest_api.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    price: Mapped[float] = mapped_column(Float(precision=2))
    desc: Mapped[str | None] = mapped_column(String)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))

    store: Mapped["StoreModel"] = relationship(back_populates="items")
    tags: Mapped[list["TagModel"]] = relationship(
        back_populates="items", secondary="items_tags"
    )
