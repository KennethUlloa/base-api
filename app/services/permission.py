from typing import List, Set
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.config.db import get_session
from app.models.permission import Permission
from app.models.tables import role_permission
from app.models.user import User


class PermissionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role_permission_names(self, role_id: str | UUID) -> Set[str]:
        """
        Obtiene todos los nombres de permisos asignados al rol,
        incluyendo todos los descendientes recursivos usando un CTE.
        """
        # Alias para la tabla Permission
        perm_alias = aliased(Permission)

        # CTE recursivo
        cte = (
            select(Permission.id, Permission.name, Permission.parent_id)
            .join(role_permission, role_permission.c.permission_id == Permission.id)
            .where(role_permission.c.role_id == str(role_id))
            .cte(name="perms_cte", recursive=True)
        )

        cte_alias = aliased(cte)

        cte = cte.union_all(
            select(Permission.id, Permission.name, Permission.parent_id)
            .join(cte_alias, Permission.parent_id == cte_alias.c.id)
        )

        result = await self.session.execute(select(cte.c.name))
        return {row[0] for row in result.all()}

    async def has_any_permission(self, role_id: str | UUID, names: List[str]) -> bool:
        permission_names = await self.get_role_permission_names(role_id)
        return any(name in permission_names for name in names)

    async def has_all_permissions(self, role_id: str | UUID, names: List[str]) -> bool:
        permission_names = await self.get_role_permission_names(role_id)
        return all(name in permission_names for name in names)

    async def user_has_any_permission(self, user: User, names: List[str]) -> bool:
        if not user.role_id:
            return False
        return await self.has_any_permission(user.role_id, names)

    async def user_has_all_permissions(self, user: User, names: List[str]) -> bool:
        if not user.role_id:
            return False
        return await self.has_all_permissions(user.role_id, names)


async def get_permission_service(session: AsyncSession = Depends(get_session)):
    return PermissionService(session)
