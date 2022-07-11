from fastapi import Depends, APIRouter
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User, UserCreate
from utils.auth.user import create_user

router = APIRouter(prefix='/users')


@router.post(path='/create_user', response_model=User)
async def create_user_endpoint(
        user: UserCreate,
        session: AsyncSession = Depends(get_session)):
    user = await create_user(user, session=session)
    return user