import pytest


from tests.conftest import init_db, client, anyio_backend, pytestmark
from tests.core import router
from utils.auth.password import generate_password
from schemas.user import UserLogin
from schemas.token import ResponseToken
from settings import settings


SEED = getattr(settings, 'secret_key')


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
        json=user.dict()
    )
    return ResponseToken.validate(value=response.json())