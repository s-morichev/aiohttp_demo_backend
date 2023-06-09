from http.cookies import SimpleCookie
from pathlib import Path
from typing import AsyncIterator, Awaitable, Callable, cast

import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import BaseTestServer, TestClient
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine

# Для локального запуска тестов на хосте явно загружаем переменные окружения
# из .env.test.local в корневой папке до импорта приложения, так как pytest
# сам по умолчанию загружает переменные окружения из .env
base_dir = Path(__file__).parent.parent.parent
env_test = base_dir / ".env.test.local"
load_dotenv(env_test, override=True)

from app.constants import DB_ENGINE_KEY  # noqa: E402
from app.main import init_app  # noqa: E402
from app.services import user_service  # noqa: E402
from app.tests.constants import (  # noqa: E402
    LOGIN_PATH,
    TEST_ADMIN,
    TEST_PASSWORD,
    TEST_USER,
)
from app.tests.preparation import (  # noqa: E402
    clear_all_data,
    insert_initial_data,
)

AiohttpClient = Callable[
    [web.Application | BaseTestServer], Awaitable[TestClient]
]


@pytest_asyncio.fixture
async def app() -> AsyncIterator[web.Application]:
    application = await init_app()
    runner = web.AppRunner(application, handle_signals=True)
    await runner.setup()  # call appliction.on_startup coroutines

    await clear_all_data(application)
    await insert_initial_data(application)

    yield application

    await runner.cleanup()  # call appliction.on_cleanup coroutines


@pytest_asyncio.fixture
async def engine(app: web.Application) -> AsyncEngine:
    return cast(AsyncEngine, app[DB_ENGINE_KEY])


@pytest_asyncio.fixture
async def test_user_id(app: web.Application) -> str:
    async with app[DB_ENGINE_KEY].connect() as conn:
        user = await user_service.read_user_by_login(conn, TEST_USER)
    if user is None:
        raise RuntimeError("Test user not created")
    return str(user.id)


@pytest_asyncio.fixture
async def test_admin_id(app: web.Application) -> str:
    async with app[DB_ENGINE_KEY].connect() as conn:
        user = await user_service.read_user_by_login(conn, TEST_ADMIN)
    if user is None:
        raise RuntimeError("Test admin not created")
    return str(user.id)


@pytest_asyncio.fixture
async def client(
    app: web.Application, aiohttp_client: AiohttpClient
) -> TestClient:
    return await aiohttp_client(app)


@pytest_asyncio.fixture
async def user_cookie_session(client: TestClient) -> SimpleCookie[str]:
    url = LOGIN_PATH
    response = await client.post(
        url,
        json={
            "login": TEST_USER,
            "password": TEST_PASSWORD,
        },
    )
    return response.cookies


@pytest_asyncio.fixture
async def admin_cookie_session(client: TestClient) -> SimpleCookie[str]:
    url = LOGIN_PATH
    response = await client.post(
        url,
        json={
            "login": TEST_ADMIN,
            "password": TEST_PASSWORD,
        },
    )
    return response.cookies


@pytest_asyncio.fixture
async def client_admin(
    client: TestClient, admin_cookie_session: SimpleCookie[str]
) -> TestClient:
    client.session.cookie_jar.update_cookies(admin_cookie_session)
    return client
