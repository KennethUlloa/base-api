from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.base import DTO
from app.schemas.permission import PermissionDTO


class RoleDTO(DTO):
    id: UUID
    name: str
    description: str
    permissions: list | None = Field(default=[])

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            permissions=[
                PermissionDTO.from_model(permission) for permission in model.permissions
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
