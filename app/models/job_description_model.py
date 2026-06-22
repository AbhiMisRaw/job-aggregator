
from sqlalchemy import (
    String,
    Integer,
    Double,
    Boolean,
    DateTime
    )
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )
from .base import Base


class JobDescription(Base):
    __tablename__ = "job_description"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(5000)) # for Text datatype in sql
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    salary_min: Mapped[float] = mapped_column(Double(7))
    salary_max: Mapped[float] = mapped_column(Double(7))
    min_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    max_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    employment_type: Mapped[str] = mapped_column(String(50))
    remote_type: Mapped[str] = mapped_column(String(50))
    
    job_link_id: Mapped[int] = mapped_column(
        ForeignKey("job_listings.id"),
        unique=True,
    )

    job_link: Mapped["JobListing"] = relationship(
        back_populates="job_description"
    )
    skills: Mapped["Skill"] = relationship(
        secondary="job_skills",
        back_populates="jobs"
    )

