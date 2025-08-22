from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.db import DBModel


class Permission(DBModel):
    __tablename__ = "permissions"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    
    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("permissions.id"), nullable=True
    )

    parent: Mapped["Permission | None"] = relationship(
        "Permission",
        remote_side="Permission.id",
        back_populates="children",
        lazy="selectin",
        default=None
    )

    children: Mapped[list["Permission"]] = relationship(
        "Permission",
        back_populates="parent",
        lazy="selectin",
        default_factory=list
    )
