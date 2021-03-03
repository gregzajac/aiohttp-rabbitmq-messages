import pytest
from api import create_app


@pytest.fixture
async def client(aiohttp_client):
    app = create_app("testing")
    return await aiohttp_client(app)


@pytest.fixture
def info():
    return "fix"
