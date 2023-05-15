import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from app import schemas
from app.db.tables import history
from app.services import user_service

pytestmark = pytest.mark.asyncio


async def test_save_user_update_history(
    engine: AsyncEngine, test_user_id: str
) -> None:
    user_update = schemas.UserUpdate(name="username")
    stmt = sa.select(history)
    async with engine.begin() as conn:
        await user_service.update_user(conn, test_user_id, user_update)
        change_result = await conn.execute(stmt)
        change = change_result.mappings().first()

    assert change
    assert change["new"]["name"] == "username"
