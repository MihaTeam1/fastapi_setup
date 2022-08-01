from sqlmodel import Enum, Field, Relationship, SQLModel
from sqlalchemy import Column, String
import enum
from typing import Optional, List
from uuid import UUID

from .base import ModelBase as Base
from .links import UserPermissionLink
from .register import PermissionRegistered

PermissionCRUD = enum.Enum('PermissionCRUD', PermissionRegistered().models)


class PermissionBase(SQLModel):
    perm: PermissionCRUD
    description: Optional[str]


class Permission(Base, PermissionBase, table=True):
    perm: PermissionCRUD = Field(sa_column=Column(
        String,
        nullable=False
    ))
    users: List['User'] = Relationship(
        back_populates='permissions',
        link_model=UserPermissionLink
    )
