from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient

from app.config import settings
from app.tests import constants

pytestmark = pytest.mark.asyncio

ROLES_PATH = constants.ROLES_PATH
ROLES_NAME_PATH = "".join((ROLES_PATH, "/{name}"))
NAME_KEY = "name"


async def test_create_role(client_admin: TestClient) -> None:
    url = ROLES_PATH
    response = await client_admin.post(
        url, json={NAME_KEY: constants.TEST_ROLE}
    )
    assert response.status == HTTPStatus.CREATED
    role = await response.json()
    assert role.get(NAME_KEY) == constants.TEST_ROLE


async def test_read_role(client_admin: TestClient) -> None:
    url = ROLES_NAME_PATH.format(name=settings.default_role)
    response = await client_admin.get(url)
    assert response.status == HTTPStatus.OK
    role = await response.json()
    assert role.get(NAME_KEY) == settings.default_role


async def test_delete_used_role(
    client_admin: TestClient,
) -> None:
    url = ROLES_NAME_PATH.format(name=settings.default_role)
    response = await client_admin.delete(url)
    assert response.status == HTTPStatus.CONFLICT


async def test_delete_unused_role(
    client_admin: TestClient,
) -> None:
    url = ROLES_NAME_PATH.format(name=constants.TEST_ROLE)
    # create role
    await client_admin.post(ROLES_PATH, json={NAME_KEY: constants.TEST_ROLE})
    # delete role
    response = await client_admin.delete(url)
    assert response.status == HTTPStatus.OK

    # check role is deleted from db
    response = await client_admin.get(url)
    assert response.status == HTTPStatus.NOT_FOUND


async def test_read_roles(client_admin: TestClient) -> None:
    url = ROLES_PATH
    response = await client_admin.get(url)
    assert response.status == HTTPStatus.OK
    roles = await response.json()
    assert len(roles) == 2
