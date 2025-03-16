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
    MONGODB_DB_NAME: str

    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    CELERY_ASYNC_QUEUE_TEST_TASK_NAME: str

    CELERY_BROKER_PATH_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", use_enum_values=True)

    def model_post_init(self, __context) -> None:
        self.CELERY_BROKER_PATH_URL = f"redis://{self.REDIS_HOST_NAME}:{self.REDIS_PORT}/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_PATH: Path = Path().resolve()
