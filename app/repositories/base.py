import datetime
from typing import Generic, Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from app.config.values import NOT_MODIFIED, _NotModified
from app.config.db import DBModel, get_session

T = TypeVar("T", bound=DBModel)


class DefaultModelRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, **kwargs) -> T:
        obj = self.model(
            **{key: self.safe_value(value) for key, value in kwargs.items()}
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: str | UUID) -> T | None:
        query = self.get_one_query(id)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_page(self, page: int, page_size: int) -> tuple[list[T], int]:
        query, couent_query = self.page_query(page, page_size)
        total = (await self.session.execute(couent_query)).scalar()
        data = (await self.session.execute(query)).scalars().all()
        return data, total

    async def update(self, id: str | UUID, **kwargs) -> T | None:
        query = self.get_one_query(id)
        obj = (await self.session.execute(query)).scalar_one_or_none()
        if obj is None:
            return None
        for key, value in kwargs.items():
            if value is NOT_MODIFIED or isinstance(value, _NotModified):
                continue
            setattr(obj, key, self.safe_value(value))
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: str | UUID) -> T | None:
        query = self.get_one_query(id)
        obj = (await self.session.execute(query)).scalar_one_or_none()
        if obj is None:
            return None
        obj.deleted_at = datetime.datetime.now()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    def safe_value(self, value):
        if isinstance(value, UUID):
            return str(value)
        return value

    def page_query(self, page, page_size):
        return (
            select(self.model)
            .where(self.model.deleted_at == None)
            .limit(page_size)
            .offset((page - 1) * page_size)
        ), (
            select(func.count())
            .select_from(self.model)
            .where(self.model.deleted_at == None)
        )

    def get_one_query(self, id: str | UUID):
        return (
            select(self.model)
            .where(self.model.id == str(id), self.model.deleted_at == None)
            .limit(1)
        )


def get_model_repository(model: Type[DBModel]):
    async def _get_repo(session: AsyncSession = Depends(get_session)):
        return DefaultModelRepository(model, session)

    return _get_repo
