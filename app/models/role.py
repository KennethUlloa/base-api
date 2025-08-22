from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db import DBModel
from app.models.tables import role_permission
from app.models.permission import Permission


class Role(DBModel):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permission,
        init=False,
        lazy="selectin",
    )
