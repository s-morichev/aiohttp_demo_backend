from http import HTTPStatus
from http.cookies import SimpleCookie

import pytest
from aiohttp.test_utils import TestClient

from app.config import settings
from app.tests.constants import (
    LOGIN_PATH,
    LOGOUT_PATH,
    TEST_PASSWORD,
    TEST_USER,
    USERS_PATH,
)

pytestmark = pytest.mark.asyncio


async def test_login(client: TestClient) -> None:
    url = LOGIN_PATH
    response = await client.post(
        url,
        json={
            "login": TEST_USER,
            "password": TEST_PASSWORD,
        },
    )
    assert response.status == HTTPStatus.OK
    assert settings.cookie_session_name in response.cookies


async def test_login_invalid_password(client: TestClient) -> None:
    url = LOGIN_PATH
    response = await client.post(
        url,
        json={
            "login": TEST_USER,
            "password": f"invalid{TEST_PASSWORD}",
        },
    )
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_login_invalid_login(client: TestClient) -> None:
    url = LOGIN_PATH
    response = await client.post(
        url,
        json={
            "login": f"non exist{TEST_USER}",
            "password": TEST_PASSWORD,
        },
    )
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_logout(
    client: TestClient, admin_cookie_session: SimpleCookie[str]
) -> None:
    url = LOGOUT_PATH
    client.session.cookie_jar.update_cookies(admin_cookie_session)
    response = await client.get(url)
    assert response.status == HTTPStatus.OK

    # check admin is log out
    url = USERS_PATH
    response = await client.get(url)
    assert response.status == HTTPStatus.UNAUTHORIZED
