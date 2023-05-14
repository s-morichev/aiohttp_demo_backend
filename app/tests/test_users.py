from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

from app.config import settings
from app.tests import constants

pytestmark = pytest.mark.asyncio

USERS_PATH = constants.USERS_PATH


async def test_create_user(client_admin: TestClient) -> None:
    response = await client_admin.post(
        USERS_PATH, json={"login": "test", "password": "test"}
    )
    assert response.status == HTTPStatus.CREATED
    user = await response.json()
    assert user.get("role") == settings.default_role


async def test_read_user(client_admin: TestClient, test_user_id: str) -> None:
    response = await client_admin.get(f"{USERS_PATH}/{test_user_id}")
    assert response.status == HTTPStatus.OK
    user = await response.json()
    assert user.get("role") == settings.default_role


async def test_update_user(client_admin: TestClient, test_user_id: str) -> None:
    response = await client_admin.put(
        f"{USERS_PATH}/{test_user_id}", json={"name": "username"}
    )
    assert response.status == HTTPStatus.OK

    # check user is updated in db
    response = await client_admin.get(f"{USERS_PATH}/{test_user_id}")
    assert response.status == HTTPStatus.OK
    user = await response.json()
    assert user.get("name") == "username"


async def test_update_user_password(
    client_admin: TestClient, test_user_id: str
) -> None:
    new_password = f"new{constants.TEST_PASSWORD}"
    response = await client_admin.put(
        f"{USERS_PATH}/{test_user_id}", json={"password": new_password}
    )
    assert response.status == HTTPStatus.OK

    # check password is updated in db
    response = await client_admin.post(
        "/api/v1/login",
        json={"login": constants.TEST_USER, "password": new_password},
    )
    assert response.status == HTTPStatus.OK


async def test_update_user_role(
    client_admin: TestClient, test_user_id: str
) -> None:
    new_role = "Admin"
    response = await client_admin.put(
        f"{USERS_PATH}/{test_user_id}/role", json={"name": new_role}
    )
    assert response.status == HTTPStatus.OK

    # check role is updated in db
    response = await client_admin.get(f"{USERS_PATH}/{test_user_id}")
    assert response.status == HTTPStatus.OK
    user = await response.json()
    assert user.get("role") == new_role


async def test_delete_user(client_admin: TestClient, test_user_id: str) -> None:
    response = await client_admin.delete(f"{USERS_PATH}/{test_user_id}")
    assert response.status == HTTPStatus.OK

    # check user is deleted from db
    response = await client_admin.get(f"{USERS_PATH}/{test_user_id}")
    assert response.status == HTTPStatus.NOT_FOUND


async def test_read_users(client_admin: TestClient) -> None:
    response = await client_admin.get(USERS_PATH)
    assert response.status == HTTPStatus.OK
    users = await response.json()
    assert len(users) == 2