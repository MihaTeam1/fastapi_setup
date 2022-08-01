from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String
from typing import List, TYPE_CHECKING

from .base import IDModelBase as Base
from .register import register
from .links import GroupUserLink

if TYPE_CHECKING:
    from .token import TokenModel
    from .group import GroupModel


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


@register
class UserModel(Base, UserBaseWithPassword, table=True):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    is_superuser: bool = False
    tokens: List['TokenModel'] = Relationship(back_populates='user')
    groups: List['GroupModel'] = Relationship(
        back_populates='members',
        link_model=GroupUserLink
    )









