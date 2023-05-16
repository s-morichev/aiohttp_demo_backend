from datetime import date, datetime
from uuid import UUID

from pydantic import Field

from app.constants import USER_LOGIN_LEN, USER_NAME_LEN, USER_SURNAME_LEN
from app.schemas.base import BaseSchema


class User(BaseSchema):
    id: UUID
    name: str
    surname: str
    birthdate: date | None
    registered_at: datetime
    role: str


class UserInDB(User):
    login: str
    password_hash: str


class UserCreate(BaseSchema):
    login: str = Field(..., max_length=USER_LOGIN_LEN)
    password: str


class UserUpdate(BaseSchema):
    password: str | None = None
    name: str | None = Field(None, max_length=USER_NAME_LEN)
    surname: str | None = Field(None, max_length=USER_SURNAME_LEN)
    birthdate: date | None
