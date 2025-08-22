from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.routes.helpers import or_404, value_or_404
from app.repositories.base import DefaultModelRepository, get_model_repository
from app.schemas.base import PageResponse, Message
from app.schemas.user import UserDTO, UserCreate, UserUpdate
from app.models.user import User
from app.security.auth import user_with_any


router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserDTO, status_code=201)
async def create_user(
    user: UserCreate,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
    _=Depends(user_with_any(["users:create"])),
) -> UserDTO:
    return await repo.create(**user.model_dump())


@router.get("/me", response_model=UserDTO)
async def get_current_user(
    user: User = Depends(user_with_any(["profile:read"])),
) -> UserDTO:
    return UserDTO.from_model(user)


@router.get("/{id}", response_model=UserDTO)
async def get_user(
    id: UUID,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
    _=Depends(user_with_any(["users:read"])),
) -> UserDTO:
    return UserDTO.from_model(or_404(await repo.get(id)))


@router.get("/", response_model=PageResponse[UserDTO])
async def get_users(
    page: int = 1,
    page_size: int = 10,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
    _=Depends(user_with_any(["users:read"])),
) -> PageResponse[UserDTO]:
    data, count = await repo.get_page(page, page_size)
    dto_list = [UserDTO.from_model(user) for user in data]
    return PageResponse(data=dto_list, total=count)


@router.patch("/{id}", response_model=UserDTO)
async def update_user(
    id: UUID,
    user: UserUpdate,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
    _=Depends(user_with_any(["users:update"])),
) -> UserDTO:
    return UserDTO.from_model(or_404(await repo.update(id, **user.model_dump())))


@router.delete("/{id}", response_model=Message)
async def delete_user(
    id: UUID,
    repo: DefaultModelRepository = Depends(get_model_repository(User)),
    _=Depends(user_with_any(["users:delete"])),
) -> Message:
    return value_or_404(
        await repo.delete(id),
        Message(message="User deleted"),
        HTTPException(status_code=404, detail="User not found"),
    )
