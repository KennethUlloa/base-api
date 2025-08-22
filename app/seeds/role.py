from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.tables import role_permission
from app.models.permission import Permission

from .base import Seeder


class RoleSeeder(Seeder):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Role, session)

    async def seed(self):
        superadmin = await self.create_or_update(
            "name",
            name="super-admin",
            description="Super Admin role",
        )

        admin = await self.create_or_update(
            "name",
            name="admin",
            description="Admin role",
        )

        user = await self.create_or_update(
            "name",
            name="user",
            description="User role",
        )

        permissions = {
            superadmin.id: ["users:all", "roles:all", "permissions:all", "profile:all"],
            admin.id: ["users:all", "roles:read", "permissions:read", "profile:read"],
            user.id: ["users:read", "profile:read"],
        }

        combinations = []

        await self.session.execute(
            delete(role_permission).where(role_permission.c.role_id.in_(permissions.keys()))
        )

        for role_id in permissions:
            permissions_list = permissions[role_id]
            permission_ids = (await self.session.execute(
                select(Permission.id).where(Permission.name.in_(permissions_list))
            )).scalars().all()

            for permission_id in permission_ids:
                combinations.append((role_id, permission_id))

        await self.session.execute(
            role_permission.insert(),
            [
                {"role_id": role_id, "permission_id": permission_id}
                for role_id, permission_id in combinations
            ],
        )

        await self.session.commit()

    async def delete(self):
        await self.session.execute(delete(Role))
        await self.session.execute(delete(role_permission))
        await self.session.commit()
