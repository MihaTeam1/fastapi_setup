from sqlalchemy.ext.asyncio import AsyncSession

from schemas.permission import PermissionModel
from schemas.user import UserModel


def give_permissions_to_user(user: UserModel, perm: PermissionModel, session: AsyncSession):
    pass

def check_permission_on_action(user: UserModel, model: str, action: str):
    pass