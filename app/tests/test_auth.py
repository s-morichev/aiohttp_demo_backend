from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

pytestmark = pytest.mark.asyncio


async def test_results(client: TestClient) -> None:
    response = await client.get("/api/v1/register")
    assert response.status == HTTPStatus.OK
    assert await response.text() == "New user"
