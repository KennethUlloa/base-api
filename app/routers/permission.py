from uuid import UUID
from fastapi import APIRouter, Depends
from models.permission import Permission
from repositories.base import DefaultModelRepository, get_model_repository
from schemas.permission import PermissionDTO, PermissionCreate, PermissionUpdate
from schemas.base import Message, PageResponse
from routers.base import value_or_404, or_404


router = APIRouter(
    prefix="/permissions",
    tags=["Permission"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=PageResponse[PermissionDTO])
async def get_permissions(
    page: int = 1,
    page_size: int = 10,
    repo: DefaultModelRepository = Depends(get_model_repository(Permission)),
):
    data, total = await repo.get_page(page, page_size)
    dto_list = [PermissionDTO.from_model(permission) for permission in data]
    return PageResponse(data=dto_list, total=total)


@router.post("/", response_model=PermissionDTO, status_code=201)
async def create_permission(
    permission: PermissionCreate,
    repo: DefaultModelRepository = Depends(get_model_repository(Permission)),
):
    return PermissionDTO.from_model(await repo.create(**permission.model_dump()))


@router.get("/{id}", response_model=PermissionDTO)
async def get_permission(
    id: UUID, repo: DefaultModelRepository = Depends(get_model_repository(Permission))
):
    return PermissionDTO.from_model(or_404(await repo.get(id)))


@router.patch("/{id}", response_model=PermissionDTO)
async def update_permission(
    id: UUID,
    permission: PermissionUpdate,
    repo: DefaultModelRepository = Depends(get_model_repository(Permission)),
):
    return PermissionDTO.from_model(or_404(await repo.update(id, **permission.model_dump())))


@router.delete("/{id}", response_model=PermissionDTO)
async def delete_permission(
    id: UUID, repo: DefaultModelRepository = Depends(get_model_repository(Permission))
):
    return value_or_404(await repo.delete(id), Message(message="Permission deleted"))