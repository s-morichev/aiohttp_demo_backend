from app.schemas.base import BaseSchema


class Role(BaseSchema):
    name: str


class RoleCreate(BaseSchema):
    name: str
