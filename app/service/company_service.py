

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CompanyCareerPage,
    Platform,
)
from app.schema import (
    CompanyCareerPage,
)


class CompanyCareerPageService:

    @staticmethod
    async def get_all_companies(
        db: AsyncSession,
        platform: Platform | None = None,
    ):
        query = select(CompanyCareerPage)

        if platform:
            query = query.where(
                CompanyCareerPage.platform == platform
            )

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def create_company(
        db: AsyncSession,
        payload: CompanyCareerPageCreate,
    ):
        company = CompanyCareerPage(
            company_name=payload.company_name,
            platform=payload.platform,
            active=payload.active,
        )

        db.add(company)

        await db.commit()
        await db.refresh(company)

        return company