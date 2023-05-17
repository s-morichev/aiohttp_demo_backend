TEST_USER = "user"
TEST_ADMIN = "admin"
TEST_PASSWORD = "password"  # noqa: S105
TEST_ROLE = "role"

NAME_KEY = "name"

USERS_PATH = "/api/v1/users"
USERS_ID_PATH = "".join((USERS_PATH, "/{id}"))
USERS_ROLE_PATH = "".join((USERS_PATH, "/{id}", "/role"))

ROLES_PATH = "/api/v1/roles"
ROLES_NAME_PATH = "".join((ROLES_PATH, "/{name}"))

LOGIN_PATH = "/api/v1/login"
LOGOUT_PATH = "/api/v1/logout"
