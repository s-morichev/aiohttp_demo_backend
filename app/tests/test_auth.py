from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

from app.config import settings
from app.tests import constants

pytestmark = pytest.mark.asyncio


async def test_login(client: TestClient) -> None:
    response = await client.post(
        "/api/v1/login",
        json={
            "login": constants.TEST_USER,
            "password": constants.TEST_PASSWORD,
        },
    )
    assert response.status == HTTPStatus.OK
    assert settings.cookie_session_name in response.cookies


async def test_login_invalid_password(client: TestClient) -> None:
    response = await client.post(
        "/api/v1/login",
        json={
            "login": constants.TEST_USER,
            "password": f"invalid{constants.TEST_PASSWORD}",
        },
    )
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_login_invalid_login(client: TestClient) -> None:
    response = await client.post(
        "/api/v1/login",
        json={
            "login": f"non exist{constants.TEST_USER}",
            "password": constants.TEST_PASSWORD,
        },
    )
    assert response.status == HTTPStatus.UNAUTHORIZED
