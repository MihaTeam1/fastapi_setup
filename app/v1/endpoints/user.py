from fastapi import Depends, APIRouter, HTTPException, status
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from sqlalchemy.orm import joinedload, contains_eager
from typing import List

from utils.auth.user import create_user, login_for_access_token, get_current_user, change_password
from utils.auth.token import refresh_token, oauth2_scheme
from schemas.token import ResponseToken
from schemas.user import (
    User,
    UserCreate,
    UserChangePassword,
    UserReadWithTokens,
    UserLogin,
    UserBase,
    UserRead,
    UserReadWithPermissions
)
from models.permissions import PermissionCreate

from sqlalchemy import select

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


@router.post(path='/login', response_model=ResponseToken, name='v1.login')
async def login(
        user: UserLogin,
        session: AsyncSession = Depends(get_session)) -> ResponseToken:
    token = await login_for_access_token(user, session)
    return token


@router.get(path='/current_user', response_model=UserRead, name='v1.current_user')
async def current_user(user: User = Depends(get_current_user)):
    return user


@router.get(path='/refresh_token_endpoint', response_model=ResponseToken, name='v1.refresh_token')
async def refresh_token_endpoint(token: str = Depends(oauth2_scheme)) -> ResponseToken:
    return await refresh_token(token)


@router.post(path='/items/', response_model=List[UserReadWithPermissions], name='v1.items')
async def items(perm: PermissionCreate, session: AsyncSession = Depends(get_session)):
    u = select(User).join(User.tokens).options(contains_eager(User.tokens))
    u = await session.execute(u)
    u = u.unique().scalars().fetchall()
    return [i for i in u]