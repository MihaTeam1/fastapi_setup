from utils.auth.user import create_user, get_user

async def get_user(username: str):
    result = await get_user(username)
    return [User(**user) for user in result]

async def create_user(username: str, AsyncSession = Depends(get_session)):
    pass