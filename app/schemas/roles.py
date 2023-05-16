from pydantic import Field

from app.constants import ROLE_NAME_LEN
from app.schemas.base import BaseSchema


class Role(BaseSchema):
    name: str


class RoleCreate(BaseSchema):
    name: str = Field(..., max_length=ROLE_NAME_LEN)
