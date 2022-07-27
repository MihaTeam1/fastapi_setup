import pytest
import logging
import asyncio

from tests.conftest import init_db, client, anyio_backend, pytestmark
from tests.core import router
from tests.tests_v1.fixtures import token, user
from utils.auth.password import generate_password, verify_password
from schemas.user import UserRead
from schemas.token import ResponseToken
from settings import settings

logger = logging.getLogger(__name__)
SEED = getattr(settings, 'secret_key')


async def test_create_user_success(client, init_db):
    username = 'test'
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
    assert UserRead \
           .validate(value=response.json()) \
           .dict() \
           .keys() == response.json().keys()
    assert response.json()['username'] == 'test'


async def test_create_user_compare_passwords_fail(client, init_db):
    username = 'test'
    password = generate_password(base=username, seed=SEED, username=username)
    user = {
        'username': username,
        'password': password,
        'confirm_password': password + '#',
    }
    response = await client.post(
        router.url_path_for('v1.create_user'),
        json=user
    )
    assert response.status_code == 422
    response = response.json()
    assert 'password' in response[0]['loc']
    assert response[0]['type'] == 'validation_error'


async def test_user_create_exists(client, init_db, user):
    user = user.dict()
    user['confirm_password'] = user['password']
    response = await client.post(
        router.url_path_for('v1.create_user'),
        json=user
    )
    assert response.status_code == 400


async def test_login_success(client, init_db, user):
    user = user.dict()
    response = await client.post(
        router.url_path_for('v1.login'),
        json=user
    )
    assert response.status_code == 200
    assert ResponseToken \
        .validate(value=response.json()) \
        .dict().keys() == response.json().keys()


async def test_login_failed(client, init_db, user):
    user = user.dict()
    user['password'] = user['password'] + '#'
    response = await client.post(
        '/v1/auth/login',
        json=user
    )
    assert response.status_code == 422
    assert response.json()[0]['type'] == 'validation_error'


async def test_change_password_success(client, init_db, user, token):
    user = user.dict()
    username = user['username']
    password = user['password']
    new_password = generate_password(base=password, seed=SEED, username=username)
    response = await client.post(
        router.url_path_for('v1.change_password'),
        json={
            'password': password,
            'new_password': new_password,
            'new_confirm_password': new_password,
        },
        headers={
            'Authorization': f'Bearer {token.access_token}'
        }
    )
    assert response.status_code == 200


async def test_change_password_compare_fail(client, init_db, user, token):
    user = user.dict()
    username = user['username']
    password = user['password']
    new_password = generate_password(base=password, seed=SEED, username=username)
    response = await client.post(
        router.url_path_for('v1.change_password'),
        json={
            'password': password,
            'new_password': new_password,
            'new_confirm_password': new_password + '#',
        },
        headers={
            'Authorization': f'Bearer {token.access_token}'
        }
    )
    assert response.status_code == 422
    assert response.json()[0]['type'] == 'validation_error'


async def test_refresh_token_success(client, init_db, token):
    await asyncio.sleep(1)
    response = await client.get(
        router.url_path_for('v1.refresh_token'),
        headers={
            'Authorization': f'Bearer {token.refresh_token}'
        }
    )
    assert response.status_code == 200
    assert response.json()['access_token'] != token.access_token
    assert response.json()['refresh_token'] == token.refresh_token


async def test_refresh_token_token_type_fail(client, init_db, token):
    await asyncio.sleep(1)
    response = await client.get(
        router.url_path_for('v1.refresh_token'),
        headers={
            'Authorization': f'Bearer {token.access_token}'
        }
    )
    assert response.status_code == 403










