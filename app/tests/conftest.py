from typing import Awaitable, Callable

import pytest_asyncio
from aiohttp.test_utils import BaseTestServer, TestClient
from aiohttp.web import Application

from app.main import init_app

AiohttpClient = Callable[[Application | BaseTestServer], Awaitable[TestClient]]


@pytest_asyncio.fixture
async def client(aiohttp_client: AiohttpClient) -> TestClient:
    app = await init_app()
    return await aiohttp_client(app)
