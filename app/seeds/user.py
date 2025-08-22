from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete

from app.models.user import User
from app.models.role import Role
from app.security.hashing import hash_password


async def store(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def seed(session: AsyncSession) -> None:
    super_admin_role = (
        await session.execute(select(Role).where(Role.name == "super-admin"))
    ).scalar_one_or_none()

    if super_admin_role is None:
        raise Exception("Super admin role not found: super-admin")

    await store(
        session,
        User(
            username="superadmin",
            password=hash_password("123456789"),
            role_id=super_admin_role.id,
            first_name="Super",
            last_name="Admin",
            email="superadmin@testing",
        ),
    )

    admin_role = (
        await session.execute(select(Role).where(Role.name == "admin"))
    ).scalar_one_or_none()

    if admin_role is None:
        raise Exception("Admin role not found: admin")

    await store(
        session,
        User(
            username="admin",
            password=hash_password("123456789"),
            role_id=admin_role.id,
            first_name="Admin",
            last_name="User",
            email="admin@testing",
        ),
    )

    await session.commit()


async def delete(session: AsyncSession) -> None:
    await session.execute(sql_delete(User))
    await session.commit()
