import pytest
from httpx import AsyncClient

from . import test_db
from .core import app


@pytest.fixture(scope='function')
async def init_db():
    await test_db.init_db()


@pytest.fixture(scope='session')
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'

pytestmark = pytest.mark.anyio