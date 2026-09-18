from sqlalchemy import Column, Integer, String

from py_rest_api.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
