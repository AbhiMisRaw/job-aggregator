from pydantic import BaseModel
from datetime import datetime
from app.models import Platform


class CompanyCareerPageCreate(BaseModel):
    comapny_name: str
    career_page_url: str
    platform: Platform

class CompanyCareerPage(BaseModel):
    id: str
    company_name: str
    company_url: str

    platform: Platform
    active: bool
    is_delete: bool

    created_at : datetime
    updated_at : datetime