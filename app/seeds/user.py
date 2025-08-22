from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete

from app.models.user import User
from app.models.role import Role
from app.security.hashing import hash_password
from .base import Seeder

class UserSeeder(Seeder):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def seed(self) -> None:
        roles = await self.session.execute(select(Role))
        roles_map = {role.name: role.id for role in roles.scalars().all()}

        if "super-admin" not in roles_map:
            raise Exception("Super admin role not found: super-admin")

        await self.create_or_update(
            "username",
            username="superadmin",
            password=hash_password("123456789"),
            role_id=roles_map["super-admin"],
            first_name="Super",
            last_name="Admin",
            email="superadmin@email.com",
        )

        if "admin" not in roles_map:
            raise Exception("Admin role not found: admin")

        await self.create_or_update(
            "username",
            username="admin",
            password=hash_password("123456789"),
            role_id=roles_map["admin"],
            first_name="Admin",
            last_name="User",
            email="admin@email.com",
        )

        if "user" not in roles_map:
            raise Exception("User role not found: user")
        
        await self.create_or_update(
            "username",
            username="user",
            password=hash_password("123456789"),
            role_id=roles_map["user"],
            first_name="User",
            last_name="User",
            email="user@email.com",
        )
