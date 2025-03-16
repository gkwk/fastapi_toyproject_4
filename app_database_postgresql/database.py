from typing import Annotated, Optional, Callable, TypeVar

import contextlib
import functools
import os

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from app_database_postgresql.configurations.configuration import get_settings, rdbms_naming_convention

F = TypeVar("F", bound=Callable)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=rdbms_naming_convention)


connect_args = {}
engine: AsyncEngine = create_async_engine(
    get_settings().RDB_PATH_URL, connect_args=connect_args, pool_pre_ping=True, pool_recycle=36000
)

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=True)


async def database_engine_shutdown():
    global engine
    if engine:
        await engine.dispose()


async def get_database():
    database = async_session_factory()
    try:
        yield database
    except Exception as e:
        await database.rollback()
        raise e
    finally:
        await database.close()


@contextlib.asynccontextmanager
async def get_database_for_decorator():
    database = async_session_factory()
    try:
        yield database
    except Exception as e:
        database.rollback()
        raise e
    finally:
        database.close()


async def get_database_decorator(function: F) -> F:
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        async with get_database_for_decorator() as database:
            return await function(*args, database=database, **kwargs)

    return wrapper
