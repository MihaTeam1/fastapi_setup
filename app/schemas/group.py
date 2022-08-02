from typing import List
from pydantic import BaseModel

from models.group import GroupModel, GroupBase, Base


class GroupRead(Base, GroupBase):
    pass


class GroupCreate(GroupBase):
    pass

class AddUserToGroup(BaseModel):
    user_id: int
    group_id: int

class GroupReadWithUsers(GroupRead):
    from schemas.user import UserRead
    users: List[UserRead] = []


class GroupReadWithPermission(GroupRead):
    from schemas.permission import PermissionRead
    permissions: List[PermissionRead] = []


class GroupReadWithUsersAndPermissions(GroupReadWithUsers, GroupReadWithPermission):
    pass
