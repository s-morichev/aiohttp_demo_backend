from http.cookies import SimpleCookie
from pathlib import Path
from typing import Awaitable, Callable

import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import BaseTestServer, TestClient
from dotenv import load_dotenv

# Для запуска тестов на хосте явно загружаем переменные окружения
# из .env.test в корневой папке до импорта приложения, так как pytest
# сам по умолчанию загружает переменные окружения из .env
# TODO настроить тестирование в докере
base_dir = Path(__file__).parent.parent.parent
env_test = base_dir / ".env.test"
load_dotenv(env_test, override=True)


from app import schemas, user_service  # noqa: E402p
from app.main import init_app  # noqa: E402
from app.tests import constants  # noqa: E402

AiohttpClient = Callable[
    [web.Application | BaseTestServer], Awaitable[TestClient]
]


@pytest_asyncio.fixture
async def app() -> web.Application:
    application = await init_app()
    test_user = schemas.UserCreate(
        login=constants.TEST_USER, password=constants.TEST_PASSWORD
    )
    test_admin = schemas.UserCreate(
        login=constants.TEST_ADMIN, password=constants.TEST_PASSWORD
    )
    async with application["db_engine"].begin() as conn:
        await user_service.create_user(conn, test_user)
        await user_service.create_user(conn, test_admin, role="Admin")
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
