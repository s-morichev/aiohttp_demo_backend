from aiohttp import web
from redis.asyncio import Redis
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncEngine

from app import schemas
from app.constants import DB_ENGINE_KEY, REDIS_KEY
from app.db.tables import history, roles, users
from app.services import role_service, user_service
from app.tests import constants


async def clear_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.execute(delete(users))
        await conn.execute(delete(roles))
        await conn.execute(delete(history))


async def clear_storage(redis_client: "Redis[bytes]") -> None:
    await redis_client.flushall()


async def clear_all_data(app: web.Application) -> None:
    await clear_db(app[DB_ENGINE_KEY])
    await clear_storage(app[REDIS_KEY])


async def db_insert_initial(engine: AsyncEngine) -> None:
    admin_role = schemas.RoleCreate(name="Admin")
    user_role = schemas.RoleCreate(name="User")
    test_admin = schemas.UserCreate(
        login=constants.TEST_ADMIN, password=constants.TEST_PASSWORD
    )
    test_user = schemas.UserCreate(
        login=constants.TEST_USER, password=constants.TEST_PASSWORD
    )

    async with engine.begin() as conn:
        await role_service.create_role(conn, admin_role)
        await role_service.create_role(conn, user_role)
        await user_service.create_user(conn, test_admin, role="Admin")
        await user_service.create_user(conn, test_user)


async def insert_initial_data(app: web.Application) -> None:
    await db_insert_initial(app[DB_ENGINE_KEY])
