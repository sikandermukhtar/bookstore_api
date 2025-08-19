from config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, text, func, Boolean
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .book import Book
    from .verification_tokens import VerificationToken


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default=text("'user'")
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_img_url: Mapped[str] = mapped_column(String, nullable=True)
    is_verified: Mapped[bool] = mapped_column(
        Boolean, server_default=text("'false'"), nullable=False
    )
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
    verification_token: Mapped["VerificationToken"] = relationship(
        "VerificationToken", back_populates="user"
    )
