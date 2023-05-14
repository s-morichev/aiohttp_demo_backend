import asyncio
import contextlib

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import settings
from app.db.tables import roles, users
from app.security import get_password_hash


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
    await insert_roles(engine)
    await create_admin(engine)


async def main() -> None:
    engine = create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug_echo_sql,
    )
    with contextlib.suppress(Exception):
        await init_db(engine)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
