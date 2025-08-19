from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import DBModel


class User(DBModel):
    __tablename__ = "users"
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", lazy="selectin")