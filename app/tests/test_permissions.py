from http import HTTPStatus
from http.cookies import SimpleCookie

import pytest
from aiohttp.test_utils import TestClient

from app.tests.constants import USERS_ID_PATH

pytestmark = pytest.mark.asyncio


async def test_read_user_self(
    client: TestClient,
    test_user_id: str,
    user_cookie_session: SimpleCookie[str],
) -> None:
    url = USERS_ID_PATH.format(id=test_user_id)
    client.session.cookie_jar.update_cookies(user_cookie_session)
    response = await client.get(url)
    assert response.status == HTTPStatus.OK


async def test_read_another_user(
    client: TestClient,
    test_admin_id: str,
    user_cookie_session: SimpleCookie[str],
) -> None:
    url = USERS_ID_PATH.format(id=test_admin_id)
    client.session.cookie_jar.update_cookies(user_cookie_session)
    response = await client.get(url)
    assert response.status == HTTPStatus.FORBIDDEN


async def test_admin_read_another_user(
    client: TestClient,
    test_user_id: str,
    admin_cookie_session: SimpleCookie[str],
) -> None:
    url = USERS_ID_PATH.format(id=test_user_id)
    client.session.cookie_jar.update_cookies(admin_cookie_session)
    response = await client.get(url)
    assert response.status == HTTPStatus.OK
