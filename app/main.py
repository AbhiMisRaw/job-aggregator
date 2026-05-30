import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .models.base import Base

from .routes import (
    job_routes,
    user_routes,
    health_routes,
    career_page_routes,
)
from .db import engine

DEBUG = os.getenv("DEBUG", True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 Lifespan started")
    async with engine.begin() as conn:
        print(Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)
        print("🟢 Tables are created")

    yield

    await engine.dispose()


app = FastAPI(
    title="CrowdPulse BE",
    debug=DEBUG,
    lifespan=lifespan,
)


app.include_router(health_routes)
app.include_router(job_routes)
app.include_router(user_routes)
app.include_router(career_page_routes)

