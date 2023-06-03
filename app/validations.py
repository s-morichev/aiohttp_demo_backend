from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from pydantic import ValidationError

from app.constants import USER_ID_MUST_BE_UUID
from app.exceptions import ApiError
from app.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseSchema)  # noqa: WPS111


def is_uuid(id_: str) -> bool:
    try:
        UUID(id_)
    except ValueError:
        return False
    return True


def validate_user_id(id_: str) -> None:
    if not is_uuid(id_):
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, USER_ID_MUST_BE_UUID)


def parse_schema(encoded_bytes: bytes, schema_class: type[T]) -> T:
    try:
        schema = schema_class.parse_raw(encoded_bytes)
    except ValidationError:  # noqa: WPS329
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            f"Cannot parse schema {schema_class.__name__}",
        )
    return schema
