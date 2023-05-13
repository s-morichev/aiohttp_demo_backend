import logging

from aiohttp import web

from app.api.v1.users import user_routes
from app.db.pre_start import db_context


async def init_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(db_context)
    app.add_routes(user_routes)
    return app


if __name__ == "__main__":
    application = init_app()
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(application)
