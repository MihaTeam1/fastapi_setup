from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from v1.utils.auth.user import get_current_user
from v1.utils.auth.permission import give_permissions_to_group
from schemas.permission import PermissionCreate, PermissionRead
from schemas.user import UserModel

router = APIRouter(prefix='/permission')


@router.post(path='/give_permission', response_model=PermissionRead, name='v1.give_permission')
async def give_permission_to_user_endpoint(
        permission: PermissionCreate,
        user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    permission = await give_permissions_to_group(permission, session)
    return permission