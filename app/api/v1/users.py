from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError

from app import role_service, schemas, user_service
from app.exceptions import ApiError

user_routes = web.RouteTableDef()

DB_ENGINE_KEY = "db_engine"
USER_ID = "user_id"


@user_routes.post("/api/v1/users")
async def create_user(request: web.Request) -> web.Response:
    try:
        user_create = schemas.UserCreate.parse_raw(await request.content.read())
    except ValidationError:  # noqa: WPS329
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, "Cannot parse user")

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
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.read_user(conn, user_id)
        if not user:
            raise ApiError(HTTPStatus.NOT_FOUND, "User not found")
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.put("/api/v1/users/{user_id}")
async def update_user(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    try:
        user_update = schemas.UserUpdate.parse_raw(await request.content.read())
    except ValidationError:  # noqa: WPS329
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY, "Cannot parse user update"
        )

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.update_user(conn, user_id, user_update)
        if user is None:
            raise ApiError(HTTPStatus.NOT_FOUND, "User not found")
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.put("/api/v1/users/{user_id}/role")
async def update_user_role(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    try:
        role = schemas.Role.parse_raw(await request.content.read())
    except ValidationError:  # noqa: WPS329
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, "Cannot parse role")

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        if not await user_service.read_user(conn, user_id):
            raise ApiError(HTTPStatus.NOT_FOUND, "User not found")
        if not await role_service.read_role(conn, role.name):
            raise ApiError(HTTPStatus.NOT_FOUND, "Role not found")
        user = await user_service.update_user_role(conn, user_id, role.name)
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.delete("/api/v1/users/{user_id}")
async def delete_user(request: web.Request) -> web.Response:
    user_id = request.match_info[USER_ID]
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        user = await user_service.delete_user(conn, user_id)
        if not user:
            raise ApiError(HTTPStatus.NOT_FOUND, "User not found")
    return web.json_response(body=schemas.dump_schema(user))


@user_routes.get("/api/v1/users")
async def read_users(request: web.Request) -> web.Response:
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        users = await user_service.read_users(conn)
    return web.json_response(body=schemas.dump_schemas_sequence(users))
