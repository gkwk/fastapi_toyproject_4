from dataclasses import dataclass


@dataclass(frozen=True)
class Tags:
    INDEX = "index"
    HEALTH_CHECK = "health check"
