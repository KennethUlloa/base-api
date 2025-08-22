from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.tables import role_permission
from app.models.permission import Permission


async def store(session: AsyncSession, role: Role, permission_list: list[str]) -> Role:
    session.add(role)
    await session.commit()
    await session.refresh(role)

    permissions = (
        (
            await session.execute(
                select(Permission)
                .column(Permission.id)
                .where(Permission.name.in_(permission_list))
            )
        )
        .scalars()
        .all()
    )

    role_permissions = [
        {"role_id": role.id, "permission_id": p.id} for p in permissions
    ]

    await session.execute(role_permission.insert(), role_permissions)
    return role


async def seed(session: AsyncSession):
    await store(
        session,
        Role(name="super-admin", description="Super Admin role"),
        ["users:all", "roles:all"],
    )

    await store(
        session,
        Role(name="admin", description="Admin role"),
        ["users:all", "roles:read"],
    )


async def delete(session: AsyncSession):
    # await session.execute(role_permission.delete())
    print("Deleting roles...")
    await session.execute(sql_delete(Role))
    await session.commit()
