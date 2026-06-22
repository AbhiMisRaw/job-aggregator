from pydantic import BaseModel, Field
from typing import Optional


class JobCoreSchema(BaseModel):
    company_name: Optional[str] = Field(default=None,max_length=100)
    job_link: str = Field(max_length=150)


class JobCreationSchema(JobCoreSchema):
    pass


class JobListingSchema(JobCoreSchema):
    id: str
    valid: bool = Field(True)