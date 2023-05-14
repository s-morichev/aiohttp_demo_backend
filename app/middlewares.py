from http import HTTPStatus
from typing import Awaitable, Callable

from aiohttp import web
from aiohttp_session import get_session

from app.exceptions import ApiError
from app.security import check_permission

HandlerType = Callable[[web.Request], Awaitable[web.StreamResponse]]


@web.middleware
async def security_middleware(
    request: web.Request, handler: HandlerType  # noqa: WPS110
) -> web.StreamResponse:
    session = await get_session(request)
    if request.path == "/api/v1/login":
        return await handler(request)

    if session.new:
        raise ApiError(HTTPStatus.UNAUTHORIZED, "Unauthorized")

    if not check_permission(request, session):
        raise ApiError(HTTPStatus.FORBIDDEN, "Forbidden")

    return await handler(request)


@web.middleware
async def error_middleware(
    request: web.Request, handler: HandlerType  # noqa: WPS110
) -> web.StreamResponse:
    try:
        return await handler(request)
    except ApiError as error:
        return web.json_response(
            {"msg": error.detail}, status=error.status_code
        )
    except web.HTTPInternalServerError:
        return web.json_response(
            {"msg": "Internal server error"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
