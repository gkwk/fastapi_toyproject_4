from dataclasses import dataclass, asdict
from typing import Optional, TypeVar, Any, Type, ClassVar

from bson import ObjectId

from commons.enums import MongoDBCollectionName

T = TypeVar("T", bound="BaseMongoDBWrapper")


@dataclass
class BaseMongoDBWrapper:
    """
    MongoDB 모델 Wrapper 기본 클래스
    """

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> Optional[T]:
        return cls(**data) if data else None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LLMPrompt(BaseMongoDBWrapper):

    system: str
    user: str
    assistant: str

    _id: Optional[ObjectId] = None


@dataclass
class TextToImageModelPrompt(BaseMongoDBWrapper):

    positive: str
    negative: str
    seed: int

    _id: Optional[ObjectId] = None
