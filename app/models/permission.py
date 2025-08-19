from typing import Self
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import DBModel
from models.tables import role_permission


class Permission(DBModel):
    __tablename__ = "permissions"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # 🔽 self reference => parent permission (optional)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("permissions.id"), nullable=True
    )
    parent: Mapped["Permission | None"] = relationship(
        "Permission",
        remote_side="Permission.id",
        backref="children",
        lazy="selectin",
        init=False
    )

    # many-to-many backref to Role
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=role_permission,
        back_populates="permissions",
        init=False,
        lazy="selectin"
    )
