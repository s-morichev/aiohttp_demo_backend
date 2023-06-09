from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError

from app import schemas
from app.constants import DB_ENGINE_KEY
from app.exceptions import ApiError
from app.services import auth_service, user_service

auth_routes = web.RouteTableDef()


@auth_routes.post("/api/v1/login")
async def login(request: web.Request) -> web.Response:
    try:
        creds = schemas.LoginPasswordCreds.parse_raw(
            await request.content.read()
        )
    except ValidationError:  # noqa: WPS329
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY, "Cannot parse login password"
        )

    async with request.app[DB_ENGINE_KEY].connect() as conn:
        user = await user_service.read_user_by_login(conn, creds.login)

    response = web.json_response()
    return await auth_service.login_user(user, creds, request, response)


@auth_routes.get("/api/v1/logout")
async def logout(request: web.Request) -> web.Response:
    response = web.json_response()
    return await auth_service.logout_user(request, response)
