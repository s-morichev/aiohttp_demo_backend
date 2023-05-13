from aiohttp import web

from app import user_service
from app.schemas import dump_schemas_list

user_routes = web.RouteTableDef()


@user_routes.get("/api/v1/users")
async def read_users(request: web.Request) -> web.Response:
    async with request.app["db_engine"].connect() as conn:
        users = await user_service.read_users(conn)
        return web.json_response(body=dump_schemas_list(users))
