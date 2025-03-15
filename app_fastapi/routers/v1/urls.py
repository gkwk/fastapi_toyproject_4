from dataclasses import dataclass


@dataclass(frozen=True)
class Prefixes:
    API_ROUTER = ""

    USERS_ROUTER = "/users"


@dataclass(frozen=True)
class Endpoints:
    ENDPOINT = ""
    ENDPOINT_SLASH = "/"
