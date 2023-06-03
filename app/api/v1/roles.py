from http import HTTPStatus

from aiohttp import web

from app import schemas
from app.constants import DB_ENGINE_KEY, ROLE_NAME
from app.exceptions import ApiError
from app.services import role_service
from app.validations import parse_schema

role_routes = web.RouteTableDef()


@role_routes.post("/api/v1/roles")
async def create_role(request: web.Request) -> web.Response:
    role_create = parse_schema(await request.content.read(), schemas.RoleCreate)

    async with request.app[DB_ENGINE_KEY].begin() as conn:
        role = await role_service.create_role(conn, role_create)
        if role is None:
            raise ApiError(HTTPStatus.CONFLICT, "Role already exist")
    return web.json_response(
        body=schemas.dump_schema(role), status=HTTPStatus.CREATED
    )


@role_routes.get("/api/v1/roles/{role_name}")
async def read_role(request: web.Request) -> web.Response:
    role_name = request.match_info[ROLE_NAME]
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        role = await role_service.read_role(conn, role_name)
        if not role:
            raise ApiError(HTTPStatus.NOT_FOUND, "Role not found")
    return web.json_response(body=schemas.dump_schema(role))


@role_routes.delete("/api/v1/roles/{role_name}")
async def delete_role(request: web.Request) -> web.Response:
    role_name = request.match_info[ROLE_NAME]
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        role = await role_service.delete_role(conn, role_name)
        if not role:
            raise ApiError(HTTPStatus.NOT_FOUND, "Role not found")
    return web.json_response(body=schemas.dump_schema(role))


@role_routes.get("/api/v1/roles")
async def read_roles(request: web.Request) -> web.Response:
    async with request.app[DB_ENGINE_KEY].begin() as conn:
        roles = await role_service.read_roles(conn)
    return web.json_response(body=schemas.dump_schemas_sequence(roles))
