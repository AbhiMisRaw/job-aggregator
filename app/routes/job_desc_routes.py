
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import (
    JobDescriptionCreateRequest,
    JobDescriptionList,
    JobDescriptionDetailsSchema
)
from app.db import get_db
from app.utils.security import get_current_user


router = APIRouter("/scrapped/job",tags=["Jobs"])

@router.get("/")
async def get_all_job(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pass


@router.post("/")
async def create_job(
    payload: JobDescriptionCreateRequest,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pass


@router.post("/{job_id}")
async def get_job(
    job_id: int,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pass