from http.cookies import SimpleCookie
from pathlib import Path
from typing import Awaitable, Callable

import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import BaseTestServer, TestClient
from dotenv import load_dotenv

# Для локального запуска тестов на хосте явно загружаем переменные окружения
# из .env.test.local в корневой папке до импорта приложения, так как pytest
# сам по умолчанию загружает переменные окружения из .env
base_dir = Path(__file__).parent.parent.parent
env_test = base_dir / ".env.test.local"
load_dotenv(env_test, override=True)


from app import user_service  # noqa: E402
from app.main import init_app  # noqa: E402
from app.tests import constants  # noqa: E402
from app.tests.preparation import (  # noqa: E402
    clear_all_data,
    insert_initial_data,
)

AiohttpClient = Callable[
    [web.Application | BaseTestServer], Awaitable[TestClient]
]


@pytest_asyncio.fixture
async def app() -> web.Application:
    application = await init_app()
    await clear_all_data(application)
    await insert_initial_data(application)
    return application


@pytest_asyncio.fixture
async def test_user_id(app: web.Application) -> str:
    async with app["db_engine"].connect() as conn:
        user = await user_service.read_user_by_login(conn, constants.TEST_USER)
    if user is None:
        raise RuntimeError("Test user not created")
    return str(user.id)


@pytest_asyncio.fixture
async def test_admin_id(app: web.Application) -> str:
    async with app["db_engine"].connect() as conn:
        user = await user_service.read_user_by_login(conn, constants.TEST_ADMIN)
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
    response = await client.post(
        "/api/v1/login",
        json={
            "login": constants.TEST_USER,
            "password": constants.TEST_PASSWORD,
        },
    )
    return response.cookies


@pytest_asyncio.fixture
async def admin_cookie_session(client: TestClient) -> SimpleCookie[str]:
    response = await client.post(
        "/api/v1/login",
        json={
            "login": constants.TEST_ADMIN,
            "password": constants.TEST_PASSWORD,
        },
    )
    return response.cookies


@pytest_asyncio.fixture
async def client_admin(
    client: TestClient, admin_cookie_session: SimpleCookie[str]
) -> TestClient:
    client.session.cookie_jar.update_cookies(admin_cookie_session)
    return client
