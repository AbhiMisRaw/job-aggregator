from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import JobCreationSchema, JobListingSchema
from app.utils.security import get_current_user
from app.db import get_db
from app.service import JobListingService

routes = APIRouter(
    prefix="/listings/jobs",
    tags=["Jobs"]
)

@routes.post("/")
async def create_jobs(
    _body: JobCreationSchema,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = JobListingService(user)
    job = await service.create_job(_body, db=db)
    return job


@routes.get("/all")
async def get_all_jobs(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await JobListingService(user=user).get_all_jobs_by_user(db=db)


@routes.get("/")
async def get_jobs_by_company(
    company: str,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    jobs = await JobListingService(user=user).get_jobs_by_company(
        company,
        db=db
    )
    return jobs


@routes.delete("/{id}")
async def delete_job(
    id:str,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return "success" if 0 != (
        await JobListingService(user=user)
        .delete_job(id=id, db=db)
        ) else "failed"