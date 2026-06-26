from sqlalchemy import (
    String,
    Integer,
    )
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )

from .base import Base


class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        index=True
    )
    job_skills: Mapped[list["JobSkill"]] = relationship(
        back_populates="skill"
    )
