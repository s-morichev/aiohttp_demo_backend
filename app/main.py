import logging

import aiohttp_session
from aiohttp import web
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import Redis

from app.api.v1.auth import auth_routes
from app.api.v1.users import user_routes
from app.config import settings
from app.db.pre_start import create_engine, dispose_engine
from app.security import security_middleware


def setup_redis(app: web.Application) -> "Redis[bytes]":
    redis = Redis.from_url(settings.redis_uri)
    app["redis"] = redis
    return redis


async def init_app() -> web.Application:
    app = web.Application()
    await create_engine(app)
    app.on_cleanup.append(dispose_engine)
    redis = setup_redis(app)
    aiohttp_session.setup(
        app,
        RedisStorage(
            redis,
            cookie_name=settings.cookie_session_name,
            max_age=settings.cookie_session_expire_sec,
        ),
    )

    # must be after aiohttp_session setup
    app.middlewares.append(security_middleware)

    app.add_routes(user_routes)
    app.add_routes(auth_routes)
    return app


if __name__ == "__main__":
    application = init_app()
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(application)
