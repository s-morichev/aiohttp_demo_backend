from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app import schemas
from app.config import settings
from app.db.tables import users
from app.security import get_password_hash


async def create_user(
    conn: AsyncConnection,
    user_create: schemas.UserCreate,
    role: str = settings.default_role,
) -> schemas.User | None:
    existing_user = await read_user_by_login(conn, user_create.login)
    if existing_user:
        return None
    password_hash = get_password_hash(user_create.password)
    stmt = (
        insert(users)
        .values(login=user_create.login, password_hash=password_hash, role=role)
        .returning(users)
    )
    user_result = await conn.execute(stmt)
    user = user_result.one()
    return schemas.User.from_orm(user)


async def read_user(conn: AsyncConnection, user_id: str) -> schemas.User | None:
    stmt = select(users).where(users.c.id == user_id)
    user_result = await conn.execute(stmt)
    user = user_result.one_or_none()
    return schemas.User.from_orm(user) if user else None


async def read_user_by_login(
    conn: AsyncConnection, login: str
) -> schemas.UserInDB | None:
    stmt = select(users).where(users.c.login == login)
    user_result = await conn.execute(stmt)
    user = user_result.one_or_none()
    return schemas.UserInDB.from_orm(user) if user else None


async def update_user(
    conn: AsyncConnection, user_id: str, user_update: schemas.UserUpdate
) -> schemas.User | None:
    user = await read_user(conn, user_id)
    if not user:
        return None
    update_dict = user_update.dict(exclude={"password"}, exclude_unset=True)
    if user_update.password:
        password_hash = get_password_hash(user_update.password)
        update_dict["password_hash"] = password_hash
    stmt = (
        update(users).where(users.c.id == user_id).returning(users)
    )  # noqa: WPS221
    user_result = await conn.execute(stmt, update_dict)
    return schemas.User.from_orm(user_result.one())


async def update_user_role(
    conn: AsyncConnection, user_id: str, role_name: str
) -> schemas.User:
    stmt = (
        update(users)
        .where(users.c.id == user_id)
        .values(role=role_name)
        .returning(users)
    )
    user_result = await conn.execute(stmt)
    return schemas.User.from_orm(user_result.one())


async def delete_user(
    conn: AsyncConnection, user_id: str
) -> schemas.User | None:
    user = await read_user(conn, user_id)
    if not user:
        return None
    stmt = (
        delete(users).where(users.c.id == user_id).returning(users)
    )  # noqa: WPS221
    user_result = await conn.execute(stmt)
    return schemas.User.from_orm(user_result.one())


async def read_users(conn: AsyncConnection) -> list[schemas.User]:
    stmt = select(users).order_by(users.c.registered_at)
    users_result = await conn.execute(stmt)
    return [schemas.User.from_orm(user) for user in users_result.all()]
