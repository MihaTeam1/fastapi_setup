from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String

from .base import ModelBase, UUIDModelBase


class UserBase(SQLModel):
    username: str = Field(sa_column=Column(
                'username',
                String,
                unique=True,
                nullable=False,
                index=True
            ))
    password: str = Field(
                nullable=False
            )


class User(UserBase, UUIDModelBase, table=True):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

class UserCreate(UserBase):
    password2: str
