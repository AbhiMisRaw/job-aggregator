from pydantic import BaseModel, Field


class JobCoreSchema(BaseModel):
    title: str
    link_to_job: str


class JobCreationSchema(JobCoreSchema):
    pass


class JobListingSchema(JobCoreSchema):
    id: str
    valid: bool = Field(True)