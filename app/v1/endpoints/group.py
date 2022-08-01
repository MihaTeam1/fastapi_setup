from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.group import GroupCreate, GroupRead, AddUserToGroup
from v1.utils.auth.group import create_group, add_user_to_group
from v1.utils.auth.permission import RoleChecker
from db import get_session

router = APIRouter(prefix='/groups')


@router.post('/create_group',
             response_model=GroupRead,
             dependencies=[Depends(RoleChecker(
                     ['group:read', 'group:create']
                 ))]
             )
async def create_group_endpoint(group: GroupCreate, session: AsyncSession = Depends(get_session)):
    group = await create_group(group, session)
    return group


@router.post('/add_user_to_group')
async def add_user_to_groupd_endpoint(group: AddUserToGroup, session: AsyncSession = Depends(get_session)):
    await add_user_to_group(group, session)