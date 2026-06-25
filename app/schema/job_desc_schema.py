from typing import List
from pydantic import BaseModel


class JobDescriptionBaseSchema(BaseModel):
    title: str
    location: str
    min_exp: float
    max_exp: float
    employement_type: str


class JobDescriptionList(JobDescriptionBaseSchema):
    pass



class JobDescriptionDetailsSchema(JobDescriptionBaseSchema):
    content: str
    min_salary: float
    max_salary: float
    remote_type: str
    job_link: str
    skills: List[str]


class JobDescriptionCreateRequest(JobDescriptionDetailsSchema):
    company: str
    