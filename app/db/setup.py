from typing import AsyncIterator

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.constants import DB_ENGINE_KEY


async def db_engine(app: web.Application) -> AsyncIterator[None]:
    engine = create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug_echo_sql,
    )
    app[DB_ENGINE_KEY] = engine

    yield

    await app[DB_ENGINE_KEY].dispose()
