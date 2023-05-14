from pathlib import Path

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    debug: bool = Field(default=False, env="BACKEND_DEBUG")
    debug_echo_sql: bool = Field(default=False, env="BACKEND_ECHO_SQL")
    cookie_session_name: str = "session_id"
    cookie_session_expire_sec: int = 60 * 60 * 24  # 24 hours
    default_role: str = "User"
    admin_login: str = Field(..., env="BACKEND_ADMIN_LOGIN")
    admin_password: str = Field(..., env="BACKEND_ADMIN_PASSWORD")
    redis_uri: str = Field(..., env="BACKEND_REDIS_DSN")
    sqlalchemy_database_uri: str = Field(
        ...,
        env="BACKEND_PG_DSN",
    )

    @validator("sqlalchemy_database_uri", pre=True)
    def replace_scheme_to_async(cls, database_uri: str) -> str:  # noqa: N805
        return database_uri.replace("postgresql://", "postgresql+asyncpg://")

    class Config(object):
        # для запуска на хосте и дебага
        env_file = Path(__file__).parent.parent / ".env.local"


settings = Settings()
