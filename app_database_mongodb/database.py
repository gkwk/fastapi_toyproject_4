from typing import Annotated, Optional, Callable, Type, TypeVar, Any, Generic
import contextlib
import functools
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from app_database_mongodb.configurations.configuration import get_settings
from commons.enums import MongoDBCollectionName
from commons.data_wrapper.mongodb_data_wrappers import BaseMongoDBWrapper


# 타입 변수 정의

F = TypeVar("F", bound=Callable)
T = TypeVar("T", bound=BaseMongoDBWrapper)


client: AsyncIOMotorClient = AsyncIOMotorClient(get_settings().MONGODB_PATH_URL)
database: AsyncIOMotorDatabase = client.get_database(get_settings().MONGODB_DB_NAME)


class MongoDBHandler:
    def __init__(self, collection_name: str | MongoDBCollectionName):
        processed_collection_name: str = collection_name

        if isinstance(collection_name, MongoDBCollectionName):
            processed_collection_name: str = collection_name.value

        self.collection: AsyncIOMotorCollection = database.get_collection(processed_collection_name)

    async def get(self, key: str) -> dict[str, Any]:
        """
        ObjectId로 문서 조회
        """
        bson = await self.collection.find_one({"_id": ObjectId(key)})
        return bson

    async def set(self, value: dict) -> str:
        """
        문서 삽입
        """
        result = await self.collection.insert_one(value)
        return str(result.inserted_id)

    async def delete(self, key: str) -> None:
        """
        문서 삭제
        """
        await self.collection.delete_one({"_id": ObjectId(key)})

    async def exist(self, key: str) -> bool:
        """
        문서 존재 여부 확인
        """
        bson = await self.collection.find_one({"_id": ObjectId(key)})
        return bson is not None


async def mongodb_client_shutdown():
    global client
    if client:
        client.close()


@contextlib.asynccontextmanager
async def get_mongodb_handler(collection_name: str | MongoDBCollectionName):
    """
    컨텍스트 매니저로 핸들러 제공
    """
    handler = MongoDBHandler(collection_name)
    try:
        yield handler
    finally:
        pass


def get_mongodb_handler_decorator(collection_name: str | MongoDBCollectionName):
    """
    핸들러를 함수에 주입하는 데코레이터
    """

    def decorator(function: F) -> F:
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            handler = MongoDBHandler(collection_name)
            return await function(*args, mongodb=handler, **kwargs)

        return wrapper

    return decorator
