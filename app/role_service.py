from http import HTTPStatus

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from app import schemas
from app.db.tables import roles
from app.exceptions import ApiError


async def create_role(
    conn: AsyncConnection,
    role_create: schemas.RoleCreate,
) -> schemas.Role | None:
    existing_role = await read_role(conn, role_create.name)
    if existing_role:
        return None
    stmt = insert(roles).values(name=role_create.name).returning(roles)
    role_result = await conn.execute(stmt)
    role = role_result.one()
    return schemas.Role.from_orm(role)


async def read_role(
    conn: AsyncConnection, role_name: str
) -> schemas.Role | None:
    stmt = select(roles).where(roles.c.name == role_name)
    role_result = await conn.execute(stmt)
    role = role_result.one_or_none()
    return schemas.Role.from_orm(role) if role else None


async def delete_role(
    conn: AsyncConnection, role_name: str
) -> schemas.Role | None:
    role = await read_role(conn, role_name)
    if not role:
        return None
    stmt = (
        delete(roles).where(roles.c.name == role_name).returning(roles)
    )  # noqa: WPS221
    try:
        role_result = await conn.execute(stmt)
    except IntegrityError:
        raise ApiError(
            HTTPStatus.CONFLICT,
            "Attempt to delete role, that referenced by some users",
        )
    return schemas.Role.from_orm(role_result.one())


async def read_roles(conn: AsyncConnection) -> list[schemas.Role]:
    stmt = select(roles).order_by(roles.c.name)
    roles_result = await conn.execute(stmt)
    return [schemas.Role.from_orm(role) for role in roles_result.all()]
