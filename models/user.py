from config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Date, Float, text, func, Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date
import enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .book import Book


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles"), nullable=False, default=UserRole.user
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_img_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    books: Mapped[List["Book"]] = relationship(
        "Book", back_populates="owner", passive_deletes=True
    )
