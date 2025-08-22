from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_session

from .base import DefaultModelRepository
from app.models.user import User


class UserRepository(DefaultModelRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        email = email.lower()
        query = select(self.model).where(self.model.email == email).limit(1)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        query = select(self.model).where(self.model.username == username).limit(1)
        return (await self.session.execute(query)).scalar_one_or_none()
    

async def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
