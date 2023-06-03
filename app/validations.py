from http import HTTPStatus
from uuid import UUID

from app.constants import USER_ID_MUST_BE_UUID
from app.exceptions import ApiError


def is_uuid(id_: str) -> bool:
    try:
        UUID(id_)
    except ValueError:
        return False
    return True


def validate_user_id(id_: str) -> None:
    if not is_uuid(id_):
        raise ApiError(HTTPStatus.UNPROCESSABLE_ENTITY, USER_ID_MUST_BE_UUID)
