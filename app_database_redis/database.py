from typing import Any, AsyncGenerator

from redis.asyncio import Redis

from app_database_redis.configurations.configuration import get_settings
from app_database_redis.redis_lua_scripts import CHECK_RATE_LIMIT_LUA_SCRIPT


class RedisHandlerAsync:
    def __init__(self):
        self._client = Redis(
            host=get_settings().REDIS_HOST_NAME,
            port=get_settings().REDIS_PORT,
            db=0,
        )

    async def get(self, key: str) -> bytes | None:
        return await self._client.get(key)

    async def set(self, key: str, value: Any, kw: dict = {}) -> None:
        await self._client.set(key, value, **kw)

    async def delete(self, key: str | list) -> None:
        await self._client.delete(key)

    async def exist(self, key: str) -> bool:
        return await key in self._client

    async def unlink(self, key: str | list) -> None:
        await self._client.unlink(key)

    async def scan(self, match: str, count: int) -> AsyncGenerator[bytes, None]:
        cursor = 0
        while True:
            cursor, keys = await self._client.scan(cursor=cursor, match=match, count=count)
            for key in keys:
                yield key

            if cursor == 0:
                break

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()

    async def incr(self, key: str) -> bytes:
        return await self._client.incr(key)

    async def xadd(self, key: str, value: dict) -> str:
        return await self._client.xadd(key, value)

    async def xlen(self, key: str) -> int:
        return await self._client.xlen(key)

    # evals

    async def check_rate_limit(
        self,
        ip_key: str,
        current_time: int,
        request_id: str,
        window_seconds: int,
        max_requests: int,
    ):
        result = await self._client.eval(
            CHECK_RATE_LIMIT_LUA_SCRIPT,
            1,
            ip_key,
            current_time,
            request_id,
            window_seconds,
            max_requests,
        )
        return result
