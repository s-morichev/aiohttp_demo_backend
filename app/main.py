import logging

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/api/v1/register")
async def register(request: web.Request) -> web.Response:
    return web.Response(text="New user")


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    application = init_app()
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(application)
