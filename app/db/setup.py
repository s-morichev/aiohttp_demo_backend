from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings


async def setup_engine(app: web.Application) -> None:
    engine = create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug_echo_sql,
    )
    app["db_engine"] = engine


async def dispose_engine(app: web.Application) -> None:
    await app["db_engine"].dispose()
