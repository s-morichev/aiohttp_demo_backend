from logging.config import dictConfig

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import Redis

from app.api.routes import setup_routes
from app.config import settings
from app.constants import REDIS_KEY
from app.db.setup import dispose_engine, setup_engine
from app.logging_config import log_config
from app.middlewares import error_middleware, security_middleware

dictConfig(log_config)


def setup_redis(app: web.Application) -> "Redis[bytes]":
    redis = Redis.from_url(settings.redis_uri)
    app[REDIS_KEY] = redis
    return redis


async def close_redis(app: web.Application) -> None:
    redis_client = app[REDIS_KEY]
    await redis_client.connection_pool.disconnect()


async def init_app() -> web.Application:
    app = web.Application()
    await setup_engine(app)
    app.on_cleanup.append(dispose_engine)
    app.on_cleanup.append(close_redis)

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
    web.run_app(application)
