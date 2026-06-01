from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CompanyCareerPage as CompanyModel,
    Platform,
)
from app.schema import (
    CompanyCareerPage,
    CompanyCareerPageCreate
)


class CompanyCareerPageService:

    @staticmethod
    async def get_all_companies(
        db: AsyncSession,
        platform: Platform | None = None,
        limit: int = 20,
        last_id: int | None = None
    ):
        query = select(CompanyModel).order_by(CompanyModel.id.asc()).limit(limit)

        if platform:
            query = query.where(
                CompanyModel.platform == platform
            )
    
        if last_id:
            # Postgres uses index scan directly, bypassing offsets completely
            query = query.where(CompanyModel.id > last_id)

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def create_company(
        payload: CompanyCareerPageCreate,
        db: AsyncSession,
        user = None,
    ):
        company = CompanyModel(
            company_name=payload.company_name,
            platform=payload.platform,
            active=True,
            company_url=payload.career_page_url
        )

        db.add(company)

        await db.commit()
        await db.refresh(company)

        return company