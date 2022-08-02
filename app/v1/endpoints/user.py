from fastapi import Depends, APIRouter, HTTPException, status
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from typing import List

from v1.utils.auth.user import create_user, get_current_user, change_password
from schemas.user import (
    UserModel,
    UserCreate,
    UserChangePassword,
    UserReadWithTokens,
    UserRead,
    UserReadWithGroupAndPermission,
)

router = APIRouter(prefix='/auth')


@router.post(path='/create_user', response_model=UserRead, name='v1.create_user')
async def create_user_endpoint(
        user: UserCreate,
        session: AsyncSession = Depends(get_session)):
    try:
        user = await create_user(user, session=session)
        return user
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')


@router.post(path='/change_password', response_model=UserRead, name='v1.change_password')
async def change_password_endpoint(
        passwords: UserChangePassword,
        user: str = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)) -> UserRead:
    return await change_password(user, passwords, session)


@router.get(path='/current_user', response_model=UserReadWithGroupAndPermission, name='v1.current_user')
async def current_user(user: UserModel = Depends(get_current_user)):
    return user


@router.get(path='/items/', response_model=List[UserReadWithTokens], name='v1.items')
async def items():#session: AsyncSession = Depends(get_session)):
    session = await anext(get_session())
    print(type(session))
    # u = select(UserModel).outerjoin(UserModel.tokens).options(contains_eager(UserModel.tokens))
    # u = await session.execute(u)
    # u = u.unique().scalars().fetchall()
    # return [i for i in u]