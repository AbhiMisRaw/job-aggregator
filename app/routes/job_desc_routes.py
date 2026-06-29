
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import (
    JobDescriptionCreateRequest,
    JobDescriptionList,
    JobDescriptionDetailsSchema
)
from app.db import get_db
from app.utils.security import get_current_user
from app.service import JobDescriptionService

routes = APIRouter(prefix="/scrapped/job",tags=["Jobs", "Job Description"])

@routes.get("/")
async def get_all_job(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pass


@routes.post("/")
async def create_job(
    payload: JobDescriptionCreateRequest,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Creates a Job."""
    return await JobDescriptionService(user, db).create_job_desc(payload)


@routes.get("/{job_id}")
async def get_job_by_id(
    job_id: int,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pass