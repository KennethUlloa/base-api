from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from .base import Seeder


class PermissionSeeder(Seeder[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(Permission, session)

    async def seed(self) -> None:

        # Users
        users = await self.create_or_update(
            "name",
            name="users:all",
            description="User management",
            parent_id=None,
        )

        await self.create_or_update(
            "name",
            name="users:read",
            description="Read users",
            parent_id=users.id,
        )

        await self.create_or_update(
            "name",
            name="users:create",
            description="Create users",
            parent_id=users.id,
        )

        await self.create_or_update(
            "name",
            name="users:update",
            description="Update users",
            parent_id=users.id,
        )

        await self.create_or_update(
            "name",
            name="users:delete",
            description="Delete users",
            parent_id=users.id,
        )

        # Roles
        roles = await self.create_or_update(
            "name",
            name="roles:all",
            description="Role management",
            parent_id=None,
        )

        await self.create_or_update(
            "name",
            name="roles:read",
            description="Read roles",
            parent_id=roles.id,
        )

        await self.create_or_update(
            "name",
            name="roles:create",
            description="Create roles",
            parent_id=roles.id,
        )

        await self.create_or_update(
            "name",
            name="roles:update",
            description="Update roles",
            parent_id=roles.id,
        )

        await self.create_or_update(
            "name",
            name="roles:delete",
            description="Delete roles",
            parent_id=roles.id,
        )

        # Permissions
        permissions = await self.create_or_update(
            "name",
            name="permissions:all",
            description="Permission management",
            parent_id=None,
        )

        await self.create_or_update(
            "name",
            name="permissions:read",
            description="Read permissions",
            parent_id=permissions.id,
        )

        await self.create_or_update(
            "name",
            name="permissions:create",
            description="Create permissions",
            parent_id=permissions.id,
        )

        await self.create_or_update(
            "name",
            name="permissions:update",
            description="Update permissions",
            parent_id=permissions.id,
        )

        await self.create_or_update(
            "name",
            name="permissions:delete",
            description="Delete permissions",
            parent_id=permissions.id,
        )

        # Profile
        profile = await self.create_or_update(
            "name",
            name="profile:all",
            description="Profile management",
            parent_id=None,
        )

        await self.create_or_update(
            "name",
            name="profile:read",
            description="Read profile",
            parent_id=profile.id,
        )

        await self.create_or_update(
            "name",
            name="profile:update",
            description="Update profile",
            parent_id=profile.id,
        )
