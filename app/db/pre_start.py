import contextlib

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import settings
from app.db.tables import metadata, roles, users
from app.security import get_password_hash


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
                    password_hash=get_password_hash(settings.admin_password),
                    role="Admin",
                ),
            )


async def init_db(engine: AsyncEngine) -> None:
    # пересоздаем таблицы пока нет миграций
    await recreate_tables(engine)
    await insert_roles(engine)
    await create_admin(engine)


async def create_engine(app: web.Application) -> None:
    engine = create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug_echo_sql,
    )
    await init_db(engine)
    app["db_engine"] = engine


async def dispose_engine(app: web.Application) -> None:
    await app["db_engine"].dispose()
