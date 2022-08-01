from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from .base import UUIDModelBase as Base
from .register import register

if TYPE_CHECKING:
    from .user import UserModel


class TokenBase(SQLModel):
    token: str = Field(
        sa_column_kwargs={'unique': True},
    )
    is_blacklisted: bool = False
    expire_in: datetime
    user_id: int = Field(foreign_key="user.id")


@register
class TokenModel(TokenBase, Base, table=True):
    __tablename__ = 'token'
    user: Optional['UserModel'] = Relationship(back_populates='tokens')







