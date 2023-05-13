from pathlib import Path
from typing import Awaitable, Callable

import pytest_asyncio
from aiohttp.test_utils import BaseTestServer, TestClient
from aiohttp.web import Application
from dotenv import load_dotenv

# Для запуска тестов на хосте явно загружаем переменные окружения
# из .env.test в корневой папке до импорта приложения, так как pytest
# сам по умолчанию загружает переменные окружения из .env
# TODO настроить тестирование в докере
base_dir = Path(__file__).parent.parent.parent
env_test = base_dir / ".env.test"
load_dotenv(env_test, override=True)


from app.main import init_app  # noqa: E402

AiohttpClient = Callable[[Application | BaseTestServer], Awaitable[TestClient]]


@pytest_asyncio.fixture
async def client(aiohttp_client: AiohttpClient) -> TestClient:
    app = await init_app()
    return await aiohttp_client(app)
