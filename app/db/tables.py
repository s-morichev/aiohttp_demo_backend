from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from app.constants import (
    ROLE_NAME_LEN,
    USER_LOGIN_LEN,
    USER_NAME_LEN,
    USER_PASSWORD_HASH_LEN,
    USER_SURNAME_LEN,
)

metadata = sa.MetaData()


roles = sa.Table(
    "roles",
    metadata,
    sa.Column("name", sa.String(ROLE_NAME_LEN), primary_key=True),
)


users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Uuid, default=uuid4, primary_key=True),
    sa.Column("name", sa.String(USER_NAME_LEN), default="", nullable=False),
    sa.Column(
        "surname", sa.String(USER_SURNAME_LEN), default="", nullable=False
    ),
    sa.Column("login", sa.String(USER_LOGIN_LEN), nullable=False, unique=True),
    sa.Column(
        "password_hash", sa.String(USER_PASSWORD_HASH_LEN), nullable=False
    ),
    sa.Column("birthdate", sa.Date),
    sa.Column(
        "registered_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.current_timestamp(),
    ),
    sa.Column(
        "role",
        sa.String(ROLE_NAME_LEN),
        sa.ForeignKey(roles.c.name),
        nullable=False,
    ),
)


history = sa.Table(
    "history",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("old", JSONB),
    sa.Column("new", JSONB),
)
