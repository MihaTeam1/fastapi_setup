import os

os.environ['SETTINGS_MODULE'] = 'test'

import pytest
from httpx import AsyncClient

from . import test_db
from .core import app
from tests.core import router
from v1.utils.auth.password import generate_password
from schemas.user import UserLogin
from schemas.token import ResponseToken
from settings import settings

SEED = getattr(settings, 'secret_key')
pytestmark = pytest.mark.anyio

@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='function')
async def init_db():
    await test_db.init_db()


@pytest.fixture(scope='session')
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='function')
async def superuser(client) -> UserLogin:
    username = 'superuser'
    password = generate_password(base=username, seed=SEED, username=username)


@pytest.fixture(scope='function')
async def superuser_token(client, superuser) -> ResponseToken:
    response = await client.post(
        router.url_path_for('v1.login'),
        json=user.dict()
    )
    return ResponseToken.validate(value=response.json())


@pytest.fixture(scope='function')
async def user(client) -> UserLogin:
    username = 'fixture'
    password = generate_password(base=username, seed=SEED, username=username)
    user = {
        'username': username,
        'password': password,
        'confirm_password': password,
    }
    response = await client.post(
        router.url_path_for('v1.create_user'),
        json=user
    )
    assert response.status_code == 200
    return UserLogin.validate(user)


@pytest.fixture(scope='function')
async def token(client, user) -> ResponseToken:
    response = await client.post(
        router.url_path_for('v1.login'),
        data=user.dict(),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    return ResponseToken.validate(value=response.json())
