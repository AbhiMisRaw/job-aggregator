from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import (
    JobDescriptionCreateRequest,
)
from app.db import get_db
from app.utils.security import get_current_user
from app.service import JobDescriptionService

routes = APIRouter(prefix="/scrapped/job",tags=["Jobs", "Job Description"])

@routes.get("/")
async def get_all_job(
    company_name: str = Query(default=None, min_length=3, max_length=15),
    min_experience: int = Query(default=0),
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    filters = {
        "company": company_name,
        min_experience: min_experience,
    }
    return await JobDescriptionService(user, db).get_job_listings(filters)


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