import os

os.environ['SETTINGS_MODULE'] = 'test'

import pytest
from httpx import AsyncClient

from . import test_db
from .core import app

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
