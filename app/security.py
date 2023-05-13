from typing import Awaitable, Callable

from aiohttp import web
from aiohttp_session import Session, get_session
from passlib.context import CryptContext

Handler = Callable[[web.Request], Awaitable[web.Response]]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_permission(request: web.Request, session: Session) -> bool:
    if session.get("role") == "Admin":
        return True
    if session.identity == request.path.replace("/api/v1/users/", ""):
        return True
    return False


@web.middleware
async def security_middleware(request: web.Request, handler: Handler) -> web.Response:
    session = await get_session(request)
    if request.path == "/api/v1/login":
        return await handler(request)

    if session.new:
        raise web.HTTPUnauthorized

    if not check_permission(session):
        raise web.HTTPForbidden

    return await handler(request)
