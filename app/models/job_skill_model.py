from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class JobSkill(Base):
    __tablename__ = "job_skills"

    job_description_id: Mapped[int] = mapped_column(
        ForeignKey("job_description.id"),
        primary_key=True
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True
    )


    job: Mapped["JobDescription"] = relationship(
        back_populates="job_skills"
    )

    skill: Mapped["Skill"] = relationship(
        back_populates="job_skills"
    )

    # job_skills: Mapped[list["JobSkill"]] = relationship(
    #     back_populates="job",
    #     cascade="all, delete-orphan"
    # )