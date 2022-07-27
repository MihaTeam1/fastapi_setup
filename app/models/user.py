from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String
from typing import List, Optional

from .base import UUIDModelBase as Base


class UserBase(SQLModel):
    username: str = Field(sa_column=Column(
                'username',
                String,
                unique=True,
                nullable=False,
                index=True
            ))


class UserBaseWithPassword(UserBase):
    password: str


class User(UserBaseWithPassword, Base, table=True):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    tokens: List['Token'] = Relationship(back_populates='user')








