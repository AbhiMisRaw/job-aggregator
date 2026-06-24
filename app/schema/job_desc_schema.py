from typing import List
from pydantic import BaseModel


class JobDescriptionBaseSchema(BaseModel):
    title: str
    location: str
    min_exp: float
    max_exp: float
    employement_type: float


class JobDescriptionList(JobDescriptionBaseSchema):
    pass


class JobDescriptionCreateRequest(JobDescriptionBaseSchema):
    content: str
    min_salary: float
    max_salary: float
    remote_type: str
    skills: List[str]


class JobDescriptionDetailsSchema(JobDescriptionCreateRequest):
    job_link: str
    