from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.tables import users


async def read_users(conn: AsyncConnection) -> list[dict[str, Any]]:
    stmt = select(users.c.login).order_by(users.c.registered_at)
    users_result = await conn.execute(stmt)
    return [dict(**user) for user in users_result.mappings().all()]


async def read_user(
    conn: AsyncConnection, user_id: str
) -> dict[str, Any] | None:
    stmt = select(users).where(users.c.id == user_id)
    user_result = await conn.execute(stmt)
    user = user_result.mappings().one_or_none()
    return dict(**user) if user else None


async def read_user_by_login(
    conn: AsyncConnection, login: str
) -> dict[str, Any] | None:
    stmt = select(users).where(users.c.login == login)
    user_result = await conn.execute(stmt)
    user = user_result.mappings().one_or_none()
    return dict(**user) if user else None
