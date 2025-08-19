from config.base import Base
from sqlalchemy import ForeignKey, String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
    token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # expire at now() + 15 minutes
    is_used: Mapped[bool] = mapped_column(
        Boolean, server_default=text("'false'"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="verification_token")
