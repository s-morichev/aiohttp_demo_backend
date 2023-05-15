from http import HTTPStatus

from aiohttp import web
from aiohttp_session import STORAGE_KEY, get_session, new_session

from app import schemas
from app.exceptions import ApiError
from app.security import verify_password


async def login_user(
    user: schemas.UserInDB | None,
    creds: schemas.LoginPasswordCreds,
    request: web.Request,
    response: web.Response,
) -> web.Response:
    if not user:
        raise ApiError(HTTPStatus.UNAUTHORIZED, "Invalid login or password")

    if not verify_password(creds.password, user.password_hash):
        raise ApiError(HTTPStatus.UNAUTHORIZED, "Invalid login or password")

    session = await get_session(request)
    storage = request.get(STORAGE_KEY)
    if storage is None:
        raise RuntimeError("Aiohttp_session not installed")

    if not session.new:
        session = await new_session(request)

    session["user_id"] = str(user.id)
    session["role"] = user.role
    await storage.save_session(request, response, session)

    return response
