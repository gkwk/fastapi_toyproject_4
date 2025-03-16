from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field

from commons.enums import AppEnviromentType


class Settings(BaseSettings):
    APP_ENVIROMENT_TYPE: AppEnviromentType

    FASTAPI_PORT: int

    RDBMS_PORT: int
    RDBMS_HOST_NAME: str
    RDBMS_USERNAME: str
    RDBMS_PASSWORD: str
    RDBMS_DB_NAME: str

    REDIS_PORT: int
    REDIS_HOST_NAME: str

    MONGODB_PORT: int
    MONGODB_HOST_NAME: str

    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    RDB_PATH_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def model_post_init(self, __context) -> None:
        self.RDB_PATH_URL = f"postgresql+asyncpg://{self.RDBMS_USERNAME}:{self.RDBMS_PASSWORD}@{self.RDBMS_HOST_NAME}:{self.RDBMS_PORT}/{self.RDBMS_DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_PATH: Path = Path().resolve()


rdbms_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
