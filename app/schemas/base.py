from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class DTO(BaseModel):
    @classmethod
    def from_model(self, model):
        raise NotImplementedError


class PageResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int


class Message(BaseModel):
    message: str
