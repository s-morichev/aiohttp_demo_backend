from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.tables import users


async def get_users(conn: AsyncConnection) -> list[dict[str, Any]]:
    stmt = select(users.c.login).order_by(users.c.registered_at)
    users_result = await conn.execute(stmt)
    return [dict(**user) for user in users_result.mappings().all()]
