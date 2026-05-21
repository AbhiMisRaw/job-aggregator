from fastapi import APIRouter, Depends
from app.schema import JobCreationSchema, JobListingSchema
from app.utils.security import get_current_user
from app.db import get_db
from app.service import JobListingService

routes = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@routes.post("/")
async def create_jobs(
    _body: JobCreationSchema,
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    service = JobListingService(user)
    job = await service.create_job(_body, db=db)
    return job


@routes.get("/all")
async def get_all_jobs():
    return [value for _, value in jobs.items()]
