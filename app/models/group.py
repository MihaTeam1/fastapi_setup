from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

from .base import IDModelBase as Base
from .links import GroupUserLink
from .register import register

if TYPE_CHECKING:
    from .user import UserModel
    from .permission import PermissionModel


class GroupBase(SQLModel):
    name: str = Field(sa_column_kwargs={
        'unique': True
    })


@register
class GroupModel(Base, GroupBase, table=True):
    __tablename__ = 'group'

    members: List['UserModel'] = Relationship(
        back_populates='groups',
        link_model=GroupUserLink
    )
    permissions: List['PermissionModel'] = Relationship(
        back_populates='group'
    )
