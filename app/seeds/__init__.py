from sqlalchemy.ext.asyncio import AsyncSession
from .permission import PermissionSeeder
from .role import RoleSeeder
from .user import UserSeeder


class SeederFacade:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.permissions = PermissionSeeder(self.session)
        self.roles = RoleSeeder(self.session)
        self.users = UserSeeder(self.session)

    async def delete(self, name: str = "all") -> None:
        if name in ["all", "users"]:
            await self.users.delete()
        if name in ["all", "roles"]:
            await self.roles.delete()
        if name in ["all", "permissions"]:
            await self.permissions.delete()
        await self.session.commit()

    async def seed(self, name: str = "all") -> None:
        if name in ["all", "permissions"]:
            await self.permissions.seed()
        if name in ["all", "roles"]:
            await self.roles.seed()
        if name in ["all", "users"]:
            await self.users.seed()
        await self.session.commit()


async def run(clean: bool = False, name: str = "all") -> None:
    from app.config.db import async_session, init_db

    await init_db()

    async with async_session() as session:
        facade = SeederFacade(session)
        if clean:
            print(f"Cleaning ({name}) database...")
            await facade.delete(name)
            print("Database cleaned")
        print(f"Seeding {name}...")
        await facade.seed(name)
