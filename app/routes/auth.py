from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.security import TokenDTO, AccessToken
from app.repositories.user import get_user_repository, UserRepository
from app.security.auth import create_access_token

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={404: {"description": "Not found"}}
)

user_repo = Depends(get_user_repository)


@router.post("/token")
async def get_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepository = user_repo,
) -> TokenDTO:
    user = await user_repo.get_by_username(form.username)
    if not user or not user.verify_password(form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenDTO(
        access_token=create_access_token(AccessToken(sub=user.id)),
        token_type="bearer",
    )
