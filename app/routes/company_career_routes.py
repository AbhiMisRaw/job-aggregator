from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import CompanyCareerPage, CompanyCareerPageCreate
from app.service import CompanyCareerPageService as Service

from app.utils.security import get_current_user
from app.utils import Params
from app.db import get_db

routes = APIRouter(
    prefix="/api/v1/company",
    tags=["Company"]
)

@routes.get("/")
async def get_all_company(
    params: Params = Depends(),
    platform: str=None,
    db: AsyncSession = Depends(get_db)
):
    return await Service.get_all_companies(
        db=db,
        platform=platform,
        limit=params.page_size,
        last_id=params.last_visited_id
        )


@routes.post("/")
async def create_company(
    career: CompanyCareerPageCreate,
    # user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    return await Service.create_company(
        user=None,
        payload=career,
        db=db
    )