from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete as sql_delete

from app.models.permission import Permission


async def store(session: AsyncSession, permission: Permission) -> Permission:
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


async def seed(session: AsyncSession):
    # users
    users_parent = await store(
        session,
        Permission(name="users:all", description="User management", parent_id=None),
    )
    await store(
        session,
        Permission("users:read", description="Read users", parent_id=users_parent.id),
    )
    await store(
        session,
        Permission(
            "users:create", description="Create users", parent_id=users_parent.id
        ),
    )
    await store(
        session,
        Permission(
            "users:update", description="Update users", parent_id=users_parent.id
        ),
    )
    await store(
        session,
        Permission(
            "users:delete", description="Delete users", parent_id=users_parent.id
        ),
    )

    # roles
    roles_parent = await store(
        session,
        Permission(name="roles:all", description="Role management", parent_id=None),
    )
    await store(
        session,
        Permission("roles:read", description="Read roles", parent_id=roles_parent.id),
    )
    await store(
        session,
        Permission(
            "roles:create", description="Create roles", parent_id=roles_parent.id
        ),
    )
    await store(
        session,
        Permission(
            "roles:update", description="Update roles", parent_id=roles_parent.id
        ),
    )
    await store(
        session,
        Permission(
            "roles:delete", description="Delete roles", parent_id=roles_parent.id
        ),
    )


async def delete(session: AsyncSession):
    await session.execute(sql_delete(Permission))
    await session.commit()
