from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.settings.base import Base
from src.task.models import Task


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tasks: Mapped[list["Task"]] = relationship()
