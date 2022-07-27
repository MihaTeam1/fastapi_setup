from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import logging

from settings import settings
from schemas.token import AccessToken, RefreshToken, ResponseToken, Token
from models.user import User


logger = logging.getLogger(__name__)

SECRET_KEY = getattr(settings, 'secret_key')
ALGORITHM = getattr(settings, 'jwt_hash_algorythm')
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'access_token_expire_minutes')
REFRESH_TOKEN_EXPIRE_MINUTES = getattr(settings, 'refresh_token_expire_minutes')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


def _create_token(
        data: dict,
        expires_delta: timedelta | int) -> dict:
    to_encode = data.copy()
    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        'token': encoded_jwt,
        'expire_in': expire,
    }


def create_access_token(
        data: dict,
        expires_delta: timedelta | int = ACCESS_TOKEN_EXPIRE_MINUTES) -> AccessToken:
    token = _create_token(data, expires_delta)
    return AccessToken(
        access_token=token['token'],
        expire_in=token['expire_in']
    )


async def create_refresh_token(
        data: dict,
        user: User,
        session: AsyncSession,
        expires_delta: timedelta | int = REFRESH_TOKEN_EXPIRE_MINUTES,
        ) -> RefreshToken:
    data['refresh'] = True
    token = _create_token(data, expires_delta)
    await add_token(
        token['token'],
        expire_in=token['expire_in'],
        user=user,
        session=session,
    )
    return RefreshToken(
        refresh_token=token['token'],
        expire_in=token['expire_in']
    )


def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def verify_token(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)


async def refresh_token(token: str):
    payload = decode_access_token(token)
    username: str = payload.get('sub')
    expire: int = payload.get('exp')
    refresh: bool = payload.get('refresh')
    if not refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You should send refresh token, or login"
        )
    access_token = create_access_token({'sub': username})
    if expire > datetime.utcnow().timestamp() \
            and expire - datetime.utcnow().timestamp() < timedelta(days=10).total_seconds():
        token = await create_refresh_token({'sub': username})
    return ResponseToken(
        access_token=access_token.token,
        refresh_token=token,
        expire_in=access_token.expire_in,
        token_type='Bearer'
    )


async def add_token(token: str, expire_in: datetime | int, user: User, session: AsyncSession):
    if isinstance(expire_in, int):
        expire_in = datetime.fromtimestamp(expire_in)
    elif isinstance(expire_in, datetime):
        pass
    else:
        raise TypeError('expire_in should be an int instance or datetime')
    token = Token(
        token=token,
        expire_in=expire_in,
        user_id=user.id,
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token


async def get_token(token: str, session: AsyncSession, only_qs=False):
    qs = select(Token).where(Token.token == token)
    if only_qs:
        return qs
    token = await session.execute(qs)
    return token.scalars().one_or_none()


async def get_tokens(tokens: List[str], session: AsyncSession, only_qs=False):
    qs = select(Token).where(Token.id.in_(tokens))
    if only_qs:
        return qs
    tokens = await session.execute(qs)
    return tokens.scalars().fetchall()


async def add_to_blacklist(token: str | Token | List[Token] | List[str], session: AsyncSession):
    if not isinstance(token, list):
        token = [token]
    str_token = []
    model_token = []
    for t in token:
        if isinstance(token, str):
            str_token.append(t)
        elif isinstance(token, Token):
            model_token.append(t)
        else:
            raise TypeError('token should be string or Token type')
    if len(str_token) == 1:
        model_token.append(await get_token(str_token[0], session))
    elif len(str_token) > 1:
        model_token.extend(await get_tokens(str_token, session))
    for token in model_token:
        token.is_blacklisted = True
    session.add_all(model_token)
    await session.commit()
    return model_token if len(model_token) > 1 else model_token[0]


