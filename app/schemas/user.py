from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

from app.schemas.base import DTO
from app.schemas.role import RoleDTO
from app.config.values import NOT_MODIFIED


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str


class UserCreate(BaseUser):
    password: str
    role_id: str


class UserUpdate(BaseUser):
    first_name: str = Field(default=NOT_MODIFIED)
    last_name: str = Field(default=NOT_MODIFIED)
    email: str = Field(default=NOT_MODIFIED)
    username: str = Field(default=NOT_MODIFIED)

    class Config:
        arbitrary_types_allowed = True


class UserDTO(DTO, BaseUser):
    id: UUID
    created_at: datetime
    updated_at: datetime
    role: RoleDTO

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_model(cls, model):
        return cls(
            id=UUID(model.id),
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            username=model.username,
            created_at=model.created_at,
            updated_at=model.updated_at,
            role=RoleDTO.from_model(model.role),
        )
