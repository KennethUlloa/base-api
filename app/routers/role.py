from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from routers.base import value_or_404, or_404
from repositories.role import get_role_repository, RoleRepository
from schemas.base import Message, PageResponse
from schemas.role import RoleCreate, RoleDTO, RoleUpdate
from models.role import Role


router = APIRouter(
    prefix="/roles", tags=["Role"], responses={404: {"description": "Not found"}}
)

_repo = Depends(get_role_repository)


@router.get("/", response_model=PageResponse[RoleDTO])
async def get_roles(
    page: int = 1,
    page_size: int = 10,
    repo: RoleRepository = Depends(get_role_repository),
):
    data, total = await repo.get_page(page, page_size)
    dto_list = [RoleDTO.from_model(role) for role in data]
    return PageResponse(data=dto_list, total=total)


@router.get("/{id}", response_model=RoleDTO)
async def get_role(id: str, repo: RoleRepository = _repo):
    return RoleDTO.from_model(or_404(await repo.get(id)))


@router.patch("/{id}", response_model=RoleDTO)
async def update_role(
    id: str,
    role: RoleUpdate,
    repo: RoleRepository = _repo,
):
    return RoleDTO.from_model(or_404(await repo.update(id, **role.model_dump())))


@router.delete("/{id}", response_model=Message)
async def delete_role(id: UUID, repo: RoleRepository = _repo):
    return value_or_404(await repo.delete(id), Message(message="Role deleted"))


@router.post("/", response_model=RoleDTO)
async def create_role(role: RoleCreate, repo: RoleRepository = _repo):
    return RoleDTO.from_model(await repo.create(**role.model_dump()))


@router.post("/{role_id}/permissions/{permission_id}", response_model=Message)
async def add_permission(
    role_id: UUID,
    permission_id: UUID,
    repo: RoleRepository = _repo,
):
    if await repo.add_permission(role_id, permission_id):
        return Message(message="Permission added")
    raise HTTPException(status_code=400, detail="Permission was not added")
