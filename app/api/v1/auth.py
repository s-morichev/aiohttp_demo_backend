from http import HTTPStatus

from aiohttp import web
from aiohttp_session import STORAGE_KEY, get_session, new_session

from app import user_service
from app.exceptions import ApiError
from app.security import verify_password

auth_routes = web.RouteTableDef()


@auth_routes.post("/api/v1/login")
async def login(request: web.Request) -> web.Response:
    session = await get_session(request)
    storage = request.get(STORAGE_KEY)
    if storage is None:
        raise RuntimeError("Aiohttp_session not installed")

    if not session.new:
        # TODO delete previous session
        # await storage.delete(session)
        session = await new_session(request)

    creds = await request.json()

    async with request.app["db_engine"].connect() as conn:
        user = await user_service.read_user_by_login(conn, creds["login"])

    if not user:
        raise ApiError(HTTPStatus.UNAUTHORIZED, "Invalid login or passowrd")

    if not verify_password(creds["password"], user.password_hash):
        raise ApiError(HTTPStatus.UNAUTHORIZED, "Invalid login or passowrd")

    response = web.json_response()
    session["user_id"] = str(user.id)
    session["role"] = user.role
    await storage.save_session(request, response, session)

    return response
