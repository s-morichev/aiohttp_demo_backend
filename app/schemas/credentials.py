from app.schemas.base import BaseSchema


class LoginPasswordCreds(BaseSchema):
    login: str
    password: str
