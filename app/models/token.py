from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional
from uuid import UUID

from .base import UUIDModelBase as Base


class TokenBase(SQLModel):
    token: str = Field(
        sa_column_kwargs={'unique': True},
    )
    is_blacklisted: bool = False
    expire_in: datetime
    user_id: UUID = Field(foreign_key="user.id")


class Token(TokenBase, Base, table=True):
    __tablename__ = 'token'
    user: Optional['User'] = Relationship(back_populates='tokens')







