# models/user.py
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )
from .base import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    link: Mapped[str] = mapped_column(
        String(150),
        index=True,
        nullable=False,
    )
    company_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )
    # relationship
    user: Mapped["User"] = relationship(
        back_populates="listings"
    )
    job_description: Mapped["JobDescription"] = relationship(
        back_populates="job_link",
        cascade="all, delete-orphan",
        uselist=False,
    )

