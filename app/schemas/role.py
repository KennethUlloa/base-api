from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.base import DTO


class RoleDTO(DTO):
    id: UUID
    name: str
    description: str
    permissions: list[str] = Field(default=[])

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            permissions=[
                permission.name for permission in model.permissions
            ],
        )


class RoleCreate(BaseModel):
    name: str
    description: str


class RoleUpdate(RoleCreate):
    pass


class AddPermission(BaseModel):
    role_id: UUID
    permission_id: UUID
