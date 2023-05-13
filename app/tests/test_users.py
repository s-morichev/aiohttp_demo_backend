from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

pytestmark = pytest.mark.asyncio


async def test_read_users(client: TestClient) -> None:
    response = await client.get("/api/v1/users")
    assert response.status == HTTPStatus.OK
    assert await response.json() == [{"login": "admin"}]
