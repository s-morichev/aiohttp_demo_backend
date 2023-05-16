from pydantic import Field

from app.constants import USER_LOGIN_LEN
from app.schemas.base import BaseSchema


class LoginPasswordCreds(BaseSchema):
    login: str = Field(..., max_length=USER_LOGIN_LEN)
    password: str
