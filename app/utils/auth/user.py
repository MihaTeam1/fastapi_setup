from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

import settings
from models.user import User, UserCreate
from exceptions.exceptions import ValidationError
from .token import decode_access_token, create_access_token
from .password import verify_password, validate_password, compare_passwords, get_password_hash


ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_by_username(username: str, session: Optional[AsyncSession] = None) -> User | None:
    qs = select(User).where(User.username == username).limit(1)
    user = await session.execute(qs)
    user = user.one_or_none()
    if not user:
        return None
    user = user.User
    return user


async def create_user(
        user: UserCreate,
        raw: bool = False,
        session: Optional[AsyncSession] = None,
        commit: bool = True) -> User | HTTPException:
    if all([session, not raw]) != any([session, not raw]):
        raise AttributeError("You should pass session or set raw = True")
    if commit and not session:
        raise AttributeError("If commit = True you should pass session")
    error = ValidationError([])
    try:
        validate_password(user.password, username=user.username)
    except ValidationError as err:
        error = ValidationError([error, err])
    try:
        compare_passwords(user.password, user.password2)
    except ValidationError as err:
        error = ValidationError({'password': [err, error]})
    if error.has_errors:
        raise error

    hashed_password = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_password)
    if not raw:
        session.add(user)
    if commit:
        await session.commit()
        await session.refresh(user)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
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
    user = get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(username: str, password: str):
    user = await get_user(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )



