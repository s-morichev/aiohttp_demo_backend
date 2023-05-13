from aiohttp import web

from app import user_service

user_routes = web.RouteTableDef()


@user_routes.get("/api/v1/users")
async def read_users(request: web.Request) -> web.Response:
    async with request.app["db_engine"].connect() as conn:
        users = await user_service.get_users(conn)
        return web.json_response(users)
