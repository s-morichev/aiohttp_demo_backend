from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.tables import users
from app.schemas import User, UserInDB


async def read_users(conn: AsyncConnection) -> list[User]:
    stmt = select(users).order_by(users.c.registered_at)
    users_result = await conn.execute(stmt)
    return [User.from_orm(user) for user in users_result.all()]


async def read_user(conn: AsyncConnection, user_id: str) -> User | None:
    stmt = select(users).where(users.c.id == user_id)
    user_result = await conn.execute(stmt)
    user = user_result.one_or_none()
    return User.from_orm(user) if user else None


async def read_user_by_login(
    conn: AsyncConnection, login: str
) -> UserInDB | None:
    stmt = select(users).where(users.c.login == login)
    user_result = await conn.execute(stmt)
    user = user_result.one_or_none()
    return UserInDB.from_orm(user) if user else None
