# models/user.py
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean, DateTime, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    link: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # relationship
    user: Mapped["User"] = relationship(
        back_populates="listings"
    )

