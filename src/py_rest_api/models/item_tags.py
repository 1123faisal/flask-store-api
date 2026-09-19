from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from py_rest_api.db import db


class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int | None] = mapped_column(ForeignKey("items.id"))
    tag_id: Mapped[int | None] = mapped_column(ForeignKey("tags.id"))
