from enum import Enum


class AppEnviromentType(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
