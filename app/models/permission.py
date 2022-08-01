from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String
import enum
from typing import Optional, TYPE_CHECKING
from pydantic import root_validator, validator

from .base import IDModelBase as Base
from .register import PermissionRegistered

PermissionCRUD = enum.Enum('PermissionCRUD', PermissionRegistered().models)

if TYPE_CHECKING:
    from .group import GroupModel


class PermissionBase(SQLModel):
    group_id: int = Field(foreign_key="user.id")
    perm: PermissionCRUD
    description: Optional[str]

    @validator('description')
    def create_desc(cls, v, values, **kwargs):
        if not v and values.get('perm'):
            desc_items = values.get('perm').split(':')
            v = f'Permission allows to {desc_items[1]} model {desc_items[0].title()}'
        return v

    @validator('perm', always=True)
    def set_perm(cls, v, values, **kwargs):
        return v.value


class PermissionModel(Base, PermissionBase, table=True):
    __tablename__ = 'permission'
    perm: PermissionCRUD = Field(sa_column=Column(
        String,
        nullable=False
    ))
    group: 'GroupModel' = Relationship(back_populates='permissions')
