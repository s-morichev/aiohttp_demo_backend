from datetime import date, datetime
from uuid import UUID

from app.schemas.base import BaseSchema


class Role(BaseSchema):
    name: str


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
    login: str
    password: str


class UserUpdate(BaseSchema):
    password: str | None = None
    name: str | None
    surname: str | None
    birthdate: date | None
