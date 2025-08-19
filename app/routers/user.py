from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from routers.base import or_404, value_or_404
from repositories.base import DefaultModelRepository, get_model_repository
from schemas.base import PageResponse, Message
from schemas.user import UserDTO, UserCreate, UserUpdate
from schemas.role import RoleDTO
from models.user import User


router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserDTO)
async def create_user(
    user: UserCreate, repo: DefaultModelRepository = Depends(get_model_repository(User))
) -> UserDTO:
    return await repo.create(**user.model_dump())


@router.get("/{id}", response_model=UserDTO)
async def get_user(
    id: UUID, repo: DefaultModelRepository = Depends(get_model_repository(User))
) -> UserDTO:
    return UserDTO.from_model(or_404(await repo.get(id)))


@router.get("/", response_model=PageResponse[UserDTO])
async def get_users(
    page: int = 1,
    page_size: int = 10,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
) -> PageResponse[UserDTO]:
    data, count = await repo.get_page(page, page_size)
    dto_list = [UserDTO.from_model(user) for user in data]
    return PageResponse(data=dto_list, total=count)


@router.patch("/{id}", response_model=UserDTO)
async def update_user(
    id: UUID,
    user: UserUpdate,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
) -> UserDTO:
    return UserDTO.from_model(or_404(await repo.update(id, **user.model_dump())))


@router.delete("/{id}", response_model=Message)
async def delete_user(
    id: UUID, repo: DefaultModelRepository = Depends(get_model_repository(User))
) -> Message:
    return value_or_404(
        await repo.delete(id),
        Message(message="User deleted"),
        HTTPException(status_code=404, detail="User not found"),
    )
