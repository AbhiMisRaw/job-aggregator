from sqlalchemy import Select
from app.models import JobListing
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound

class JobListingService():
    
    def __init__(self, user):
        self.user = user

    async def create_job(self, _body, db: AsyncSession):
        job = JobListing(link=_body.link_to_job,user_id=self.user.id)
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job


    async def get_all_jobs_by_user(self, db: AsyncSession):
        stmt = Select(JobListing).where(JobListing.user_id == self.user.id)
        result = await db.execute(stmt)
        result = result.scalars().all()
        return result if result else list()


    async def delete_job(self, id, db: AsyncSession):
        stmt = delete(JobListing).where(
            JobListing.id == id,
            JobListing.user_id == self.user.id
        )

        result = await db.execute(stmt)
        await db.commit()

        # result.rowcount tells how many rows were deleted
        return result.rowcount > 0