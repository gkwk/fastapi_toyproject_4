import contextlib

from fastapi import FastAPI

from app_database_postgresql.database import database_engine_shutdown
from app_database_mongodb.database import mongodb_client_shutdown
from app_database_redis.instance import redis_handler_async


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("START : lifespan")
    yield
    print("SHUTDOWN : PostgreSQL Connection")
    await database_engine_shutdown()
    print("SHUTDOWN : MongoDB Connection")
    await mongodb_client_shutdown()
    print("SHUTDOWN : Redis Connection")
    await redis_handler_async.close()
    print("SHUTDOWN : lifespan")
