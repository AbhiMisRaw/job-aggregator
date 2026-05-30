from fastapi import APIRouter, Depends
from app.schema import CompanyCareerPage, CompanyCareerPageCreate

from app.utils.security import get_current_user
from app.db import get_db

routes = APIRouter(
    prefix="/api/v1/company",
    tags=["Company"]
)

@routes.get("/")
async def get_all_company():
    pass


@routes.post("/")
async def create_company(
    career: CompanyCareerPageCreate,
    user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    pass