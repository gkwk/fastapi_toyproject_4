from dataclasses import dataclass


@dataclass(frozen=True)
class Prefixes:
    ROOT_ROUTER = ""

    INDEX = ""
    HEALTH_CHECK = "/health-check"


@dataclass(frozen=True)
class Endpoints:
    ENDPOINT = ""
    ENDPOINT_SLASH = "/"
