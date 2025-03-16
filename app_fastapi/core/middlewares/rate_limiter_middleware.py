import time
import uuid
from typing import Callable


from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis.exceptions

from app_database_redis.instance import redis_handler_async


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        rate_limit: int = 100,  # 시간 간격당 최대 요청 수
        time_window: int = 60,  # 시간 간격 (초)
        prefix: str = "ratelimit:",  # Redis 키 접두사
        excluded_ips: set | None = None,
    ):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.prefix = prefix
        self.excluded_ips = excluded_ips or set()

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        # IP 기반 Redis 키 생성
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        if client_ip and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()

        # 검사 예외인 IP의 경우 곧바로 다음으로 진행한다.
        if client_ip in self.excluded_ips:
            response = await call_next(request)
            return response

        ip_key = f"{self.prefix}ip:{client_ip}"

        # 현재 시간 (Unix timestamp, 단위 : s)
        current_time = int(time.time())

        # 고유 요청 ID 생성 (timestamp + uuid)
        request_id = f"{current_time}:{uuid.uuid4().hex}"

        try:
            is_allowed = await redis_handler_async.check_rate_limit(
                ip_key,
                current_time,
                request_id,
                self.time_window,
                self.rate_limit,
            )

            # 초과시 429 응답
            if not is_allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded",
                        "limit": self.rate_limit,
                        "remaining": 0,
                        "reset": current_time + self.time_window,
                    },
                )

            # 정상 처리 시 응답 생성
            response: Response = await call_next(request)

            return response

        except redis.exceptions.RedisError as e:
            print(f"Redis에서 오류가 발생하였습니다 - RateLimiterMiddleware - {e}")
            response = await call_next(request)
            return response
