import contextlib
from typing import AsyncIterator

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import settings
from app.db.tables import metadata, roles, users


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug_echo_sql,
    )


async def recreate_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


async def insert_roles(engine: AsyncEngine) -> None:
    default_roles = [{"name": "Admin"}, {"name": "User"}]
    with contextlib.suppress(IntegrityError):
        async with engine.begin() as conn:
            await conn.execute(roles.insert(), default_roles)


async def create_admin(engine: AsyncEngine) -> None:
    with contextlib.suppress(IntegrityError):
        async with engine.begin() as conn:
            await conn.execute(
                users.insert().values(
                    login=settings.admin_login,
                    password_hash="hash",
                    role="Admin",
                ),
            )


async def init_db(engine: AsyncEngine) -> None:
    # пересоздаем таблицы пока нет миграций
    await recreate_tables(engine)
    await insert_roles(engine)
    await create_admin(engine)


async def db_context(app: web.Application) -> AsyncIterator[None]:
    engine = create_engine()
    await init_db(engine)
    app["db_engine"] = engine

    yield

    await app["db_engine"].dispose()
