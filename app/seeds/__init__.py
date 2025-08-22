from sqlalchemy.ext.asyncio import AsyncSession
from . import permission, role, user


async def delete(session: AsyncSession) -> None:
    await user.delete(session)
    await role.delete(session)
    await permission.delete(session)
    await session.commit()


async def seed(session: AsyncSession) -> None:
    await permission.seed(session)
    await role.seed(session)
    await user.seed(session)
    await session.commit()


async def run(clean: bool = False) -> None:
    from app.config.db import async_session, init_db

    await init_db()

    async with async_session() as session:
        if clean:
            print("Cleaning database...")
            await delete(session)
            print("Database cleaned")
        await seed(session)
