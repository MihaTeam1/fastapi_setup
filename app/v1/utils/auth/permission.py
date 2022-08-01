from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Set

from schemas.permission import PermissionModel, AddPermissionToGroup
from schemas.user import UserModel
from v1.utils.auth.user import get_current_user


class RoleChecker:
    def __init__(self, permissions: List[str] | Set[str]):
        self.permissions = set(permissions)

    def __call__(self, user=Depends(get_current_user)):
        if user.is_superuser:
            return
        user_perms = [perm.perm for group in user.groups for perm in group.permissions]
        if len(set(user_perms) & self.permissions) != len(self.permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )


async def give_permissions_to_group(permission: AddPermissionToGroup, session: AsyncSession):
    permission = PermissionModel(
        group_id=permission.group_id,
        perm=permission.perm,
        description=permission.description
    )
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


def check_permission_on_action(user: UserModel, model: str, action: str):
    pass