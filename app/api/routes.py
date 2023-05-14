from aiohttp import web

from app.api.v1.auth import auth_routes
from app.api.v1.roles import role_routes
from app.api.v1.users import user_routes


def setup_routes(app: web.Application) -> None:
    app.add_routes(auth_routes)
    app.add_routes(role_routes)
    app.add_routes(user_routes)
