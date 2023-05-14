from datetime import date, datetime
from typing import Any, Callable, Sequence
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(
    dump_value: Any, *, default: Callable[[Any], Any] | None
) -> str:
    return orjson.dumps(dump_value, default=default).decode()


class BaseSchema(BaseModel):
    class Config(object):
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        orm_mode = True


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


def dump_schemas_list(
    models: Sequence[BaseSchema],
    default: Callable[[Any], Any] = BaseSchema.__json_encoder__,
) -> bytes:
    return orjson.dumps(models, default=default)


def dump_schema(
    model: BaseSchema,
    default: Callable[[Any], Any] = BaseSchema.__json_encoder__,
) -> bytes:
    return orjson.dumps(model, default=default)
