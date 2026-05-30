from enum import Enum

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Platform(str, Enum):
    NAUKARI = "Naukari"
    CUTSHORT = "Cutshort"
    INSTAHYRE = "Instahyre"
    CAREER_PAGE = "CareerPage"
    INDEED = "Indeed"
    OTHERS = "Others"


class CompanyCareerPage(Base):
    __tablename__ = "company_career_pages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    company_url: Mapped[str] = mapped_column(
        String(511),
        nullable=False,
    )

    platform: Mapped[Platform] = mapped_column(
        SqlEnum(Platform),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_delete: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )