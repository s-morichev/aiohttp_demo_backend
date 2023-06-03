from http import HTTPStatus

from aiohttp import web

from app import schemas
from app.constants import DB_ENGINE_KEY, USER_ID, USER_NOT_FOUND
from app.exceptions import ApiError
from app.services import role_service, user_service
from app.validations import parse_schema, validate_user_id

user_routes = web.RouteTableDef()


@user_routes.post("/api/v1/users")
async def create_user(request: web.Request) -> web.Response:
    user_create = parse_schema(await request.content.read(), schemas.UserCreate)

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.create_user(conn, user_create)
        if user is None:
            raise ApiError(HTTPStatus.CONFLICT, "User already exist")
    return web.json_response(
        body=schemas.dump_schema(user), status=HTTPStatus.CREATED
    )


@user_routes.get("/api/v1/users/{user_id}")
async def read_user(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    validate_user_id(user_id)
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.read_user(conn, user_id)
        if not user:
            raise ApiError(HTTPStatus.NOT_FOUND, USER_NOT_FOUND)
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.put("/api/v1/users/{user_id}")
async def update_user(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    validate_user_id(user_id)
    user_update = parse_schema(await request.content.read(), schemas.UserUpdate)

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.update_user(conn, user_id, user_update)
        if user is None:
            raise ApiError(HTTPStatus.NOT_FOUND, USER_NOT_FOUND)
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.put("/api/v1/users/{user_id}/role")
async def update_user_role(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    validate_user_id(user_id)
    role = parse_schema(await request.content.read(), schemas.Role)

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        if not await user_service.read_user(conn, user_id):
            raise ApiError(HTTPStatus.NOT_FOUND, USER_NOT_FOUND)
        if not await role_service.read_role(conn, role.name):
            raise ApiError(HTTPStatus.NOT_FOUND, "Role not found")
        user = await user_service.update_user_role(conn, user_id, role.name)
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.delete("/api/v1/users/{user_id}")
async def delete_user(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    validate_user_id(user_id)
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.delete_user(conn, user_id)
        if not user:
            raise ApiError(HTTPStatus.NOT_FOUND, USER_NOT_FOUND)
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.get("/api/v1/users")
async def read_users(request: web.Request) -> web.Response:
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        users = await user_service.read_users(conn)
    return web.json_response(body=schemas.dump_schemas_sequence(users))
