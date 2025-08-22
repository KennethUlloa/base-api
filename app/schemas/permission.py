from pydantic import BaseModel, Field
from uuid import UUID

from app.schemas.base import DTO


class PermissionDTO(DTO):
    id: UUID
    name: str
    description: str
    parent_id: UUID | None

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            parent_id=model.parent_id,
        )


class PermissionCreate(BaseModel):
    name: str
    description: str
    parent_id: UUID | None = Field(default=None)


class PermissionUpdate(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    parent_id: UUID | None = Field(default=None)
