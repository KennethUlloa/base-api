import datetime
import os
import uuid6
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database/app.db")

if DATABASE_URL.startswith("sqlite"):
    if not os.path.exists("./database"):
        os.makedirs("./database")


engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass

def generate_uuid():
    return str(uuid6.uuid7())

class DBModel(Base, MappedAsDataclass):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        primary_key=True, default_factory=generate_uuid, init=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        default_factory=datetime.datetime.now, init=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default_factory=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        init=False,
    )
    deleted_at: Mapped[datetime.datetime] = mapped_column(default=None, init=False, nullable=True)


async def init_db():
    from app.models.user import User
    from app.models.permission import Permission
    from app.models.role import Role

    async with engine.begin() as conn:
        await conn.run_sync(DBModel.metadata.create_all) 
