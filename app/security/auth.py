from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app.repositories.user import UserRepository, get_user_repository
from app.schemas.security import AccessToken

from app.config.values import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ALGORITHM,
    JWT_SECRET_KEY,
    TOKEN_URL,
    SUPER_ADMIN_NAME,
)
from app.services.permission import PermissionService, get_permission_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def create_token(data: dict, key: str, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(
    data: AccessToken,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    return create_token(data.model_dump(), JWT_SECRET_KEY, expires_delta)


def verify_token(token: str, credentials_exception, key):
    try:
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise credentials_exception


def get_access_token_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return AccessToken(**verify_token(token, credentials_exception, JWT_SECRET_KEY))


async def get_current_user(
    access_token_payload: AccessToken = Depends(get_access_token_payload),
    user_repo: UserRepository = Depends(get_user_repository),
):
    user = await user_repo.get(access_token_payload.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def user_with_any(permissions: list[str]):
    async def _get_user_with_permissions(
        user: User = Depends(get_current_user),
        permission_service: PermissionService = Depends(get_permission_service),
    ):
        if SUPER_ADMIN_NAME is not None and user.username == SUPER_ADMIN_NAME:
            return user
        
        if not await permission_service.user_has_any_permission(user, permissions):
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return _get_user_with_permissions


def user_with_all(permissions: list[str]):
    async def _get_user_with_permissions(
        user: User = Depends(get_current_user),
        permission_service: PermissionService = Depends(get_permission_service),
    ):
        if SUPER_ADMIN_NAME is not None and user.username == SUPER_ADMIN_NAME:
            return user
        
        if not await permission_service.user_has_all_permissions(user, permissions):
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return _get_user_with_permissions
