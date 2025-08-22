from uuid import UUID
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.db import get_session
from app.models.role import Role
from app.models.tables import role_permission
from app.repositories.base import DefaultModelRepository


class RoleRepository(DefaultModelRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)

    async def add_permission(
        self, role_id: str | UUID, permission_id: str | UUID
    ) -> bool:
        res = await self.session.execute(
            role_permission.insert().values(
                role_id=self.safe_value(role_id),
                permission_id=self.safe_value(permission_id),
            )
        )

        await self.session.commit()
        return res.rowcount > 0

    async def remove_permission(self, role_id: str | UUID, permission_id: str | UUID):
        res = await self.session.execute(
            role_permission.delete().where(
                role_permission.c.role_id == self.safe_value(role_id),
                role_permission.c.permission_id == self.safe_value(permission_id),
            )
        )

        await self.session.commit()
        return res.rowcount > 0

    def get_one_query(self, id):
        return (
            select(self.model)
            .where(self.model.id == str(id), self.model.deleted_at == None)
            .options(selectinload(self.model.permissions))
        )

    def page_query(self, page, page_size):
        return (
            select(self.model)
            .where(self.model.deleted_at == None)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .options(selectinload(self.model.permissions))
        ), (
            select(func.count())
            .select_from(self.model)
            .where(self.model.deleted_at == None)
        )


async def get_role_repository(session: AsyncSession = Depends(get_session)):
    return RoleRepository(session)
