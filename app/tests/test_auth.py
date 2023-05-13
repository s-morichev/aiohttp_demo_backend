from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

pytestmark = pytest.mark.asyncio


async def test_login(client: TestClient) -> None:
    response = await client.post(
        "/api/v1/login", json={"login": "admin", "password": "password"}
    )
    assert response.status == HTTPStatus.OK
    assert "AIOHTTP_SESSION" in response.cookies
