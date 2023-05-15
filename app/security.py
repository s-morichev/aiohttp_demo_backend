from typing import Awaitable, Callable

from aiohttp import web
from aiohttp_session import Session
from passlib.context import CryptContext

HandlerType = Callable[[web.Request], Awaitable[web.StreamResponse]]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_permission(request: web.Request, session: Session) -> bool:
    if session.get("role") == "Admin":
        return True
    return session.get("user_id") == request.path.replace("/api/v1/users/", "")
