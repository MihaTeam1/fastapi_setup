from sqlmodel import Field
from sqlalchemy import Column, String

from .base import ModelBase, UUIDModelBase


class User(UUIDModelBase, table=True):
    __tablename__ = 'users'

    name: str = Field(sa_column=Column(
                'name',
                String,
                unique=True,
                nullable=False,
                index=True
            )),
    password: str = Field(
                nullable=False
            )