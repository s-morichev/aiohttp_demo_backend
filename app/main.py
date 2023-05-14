import logging

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import Redis

from app.api.routes import setup_routes
from app.config import settings
from app.db.setup import dispose_engine, setup_engine
from app.middlewares import error_middleware, security_middleware


def setup_redis(app: web.Application) -> "Redis[bytes]":
    redis = Redis.from_url(settings.redis_uri)
    app["redis"] = redis
    return redis


async def init_app() -> web.Application:
    app = web.Application()
    await setup_engine(app)
    app.on_cleanup.append(dispose_engine)

    redis = setup_redis(app)
    redis_storage = RedisStorage(
        redis,
        cookie_name=settings.cookie_session_name,
        max_age=settings.cookie_session_expire_sec,
    )

    middlewares = [
        error_middleware,
        session_middleware(redis_storage),
        security_middleware,
    ]
    app.middlewares.extend(middlewares)

    setup_routes(app)
    return app


if __name__ == "__main__":
    application = init_app()
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(application)
