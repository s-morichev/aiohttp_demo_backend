from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

from app.config import settings
from app.tests.constants import LOGIN_PATH, TEST_PASSWORD, TEST_USER

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
