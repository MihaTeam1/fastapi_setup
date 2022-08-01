from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from v1.utils.auth.token import oauth2_scheme, refresh_token
from v1.utils.auth.user import login_for_access_token
from schemas.token import ResponseToken

router = APIRouter(prefix='/token')


@router.post(path='/login', response_model=ResponseToken, name='v1.login')
async def login(
        user: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)) -> ResponseToken:
    token = await login_for_access_token(user, session)
    return token


@router.get(path='/refresh_token_endpoint', response_model=ResponseToken, name='v1.refresh_token')
async def refresh_token_endpoint(token: str = Depends(oauth2_scheme)) -> ResponseToken:
    return await refresh_token(token)