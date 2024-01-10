from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.settings.base import Base
from datetime import date

class Task(Base):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    is_complete: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[date] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
