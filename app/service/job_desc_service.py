from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schema import (
    JobDescriptionCreateRequest,
    JobDescriptionList,
    JobDescriptionDetailsSchema
)
from .job_service import JobListingService
from app.models import JobListing, JobDescription, JobSkill, Skill

class JobDescriptionService():

    def __init__(self, user, db):
        self.user = user
        self.db = db

    async def create_job_desc(
        self,
        payload: JobDescriptionCreateRequest
    ):
        # 1. get/create job listing
        job_listing = await self._get_or_create_job_listing(
            job_link=payload.job_link,
            company=payload.company
        )

        # 2. create description
        job_description = JobDescription(
            title=payload.title,
            location=payload.location,
            description=payload.content,
            min_experience=payload.min_exp,
            max_experience=payload.max_exp,
            employment_type=payload.employement_type,
            salary_min=payload.min_salary,
            salary_max=payload.max_salary,
            remote_type=payload.remote_type,
            job_link=job_listing
        )
        # flush so job_description.id is available
        await self.db.flush()

        # 3. create skills relation
        payload.skills = [ skill.lower() for skill in payload.skills]
        for skill_name in payload.skills:
            skill = await self._get_or_create_skill(
                skill_name
            )
            job_skill = JobSkill(
                job=job_description,
                skill=skill
            )
            self.db.add(job_skill)

        await self.db.commit()
        await self.db.refresh(job_description)

        return job_description


    async def _get_or_create_job_listing(
        self,
        job_link: str,
        company: str
    ):

        result = await self.db.execute(
            select(JobListing)
            .where(
                JobListing.link == job_link,
            )
        )

        job_listing = result.scalar_one_or_none()

        if job_listing:
            # if exist return existing one.
            return job_listing
        

        job_listing = JobListing(
            link=job_link,
            company_name=company,
            user=self.user
        )

        self.db.add(job_listing)
        await self.db.flush()
        return job_listing


    async def _get_or_create_skills(
        self,
        skill_names: list[str]
    ):
        if not skill_names:
            return []

        # remove duplicates
        skill_names = list(set(skill_names))

        # 1. Fetch all existing skills in one query
        result = await self.db.execute(
            select(Skill)
            .where(
                Skill.name.in_(skill_names)
            )
        )

        existing_skills = result.scalars().all()
        existing_names = {
            skill.name
            for skill in existing_skills
        }

        # 2. Find missing skills
        new_skill_names = [
            name
            for name in skill_names
            if name not in existing_names
        ]

        # 3. Create missing skills
        new_skills = [
            Skill(name=name)
            for name in new_skill_names
        ]
        self.db.add_all(new_skills)
        # get IDs after insert
        await self.db.flush()

        return existing_skills + new_skills