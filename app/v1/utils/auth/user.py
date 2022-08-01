from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
from typing import Optional
import logging

from schemas.user import UserCreate, UserChangePassword, UserModel
from schemas.token import ResponseToken
from schemas.permission import PermissionModel
from exceptions.exceptions import ValidationError

from db import get_session
from .token import decode_access_token, create_access_token, oauth2_scheme, create_refresh_token
from .password import verify_password, get_password_hash


logger = logging.getLogger(__name__)


async def get_user_by_username(username: str, session: Optional[AsyncSession] = None) -> UserModel | None:
    qs = select(UserModel) \
            .outerjoin(UserModel.permissions) \
            .where(UserModel.username == username) \
            .limit(1) \
            .options(
                contains_eager(UserModel.permissions) \
                .load_only(PermissionModel.perm)
            )
    user = await session.execute(qs)
    user = user.unique().scalars().fetchall()
    if not user:
        return None
    return user[0]


async def create_user(
        user: UserCreate,
        raw: bool = False,
        session: Optional[AsyncSession] = None,
        commit: bool = True) -> UserModel | HTTPException:
    if all([session, not raw]) != any([session, not raw]):
        raise AttributeError("You should pass session or set raw = True")
    if commit and not session:
        raise AttributeError("If commit = True you should pass session")
    hashed_password = get_password_hash(user.password)
    user = UserModel(username=user.username, password=hashed_password)
    if not raw:
        session.add(user)
    if commit:
        await session.commit()
        await session.refresh(user)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=username, session=session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user_by_username(username, session)
    if not user or not verify_password(password, user.password):
        raise ValidationError('Invalid username or password', headers={"WWW-Authenticate": "Bearer"})
    return user


async def login_for_access_token(
        user: OAuth2PasswordRequestForm,
        session: AsyncSession) -> ResponseToken:
    user = await authenticate_user(user.username, user.password, session)
    access_token = create_access_token(
        data={'sub': user.username}
    )
    refresh_token = await create_refresh_token(
        data={'sub': user.username},
        user=user,
        session=session
    )
    return ResponseToken(
        access_token=access_token.token,
        refresh_token=refresh_token.token,
        expire_in=access_token.expire_in,
        token_type='bearer'
    )


async def change_password(user: UserModel, passwords: UserChangePassword, session: AsyncSession):
    if not verify_password(passwords.current_password, user.password):
        raise ValidationError({'password': 'Password is invalid'})
    user.password = get_password_hash(passwords.new_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

