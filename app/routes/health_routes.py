from fastapi import APIRouter, Depends
from app.db import get_db


routes = APIRouter(
    prefix="/health",
    tags=["Core"],
)


@routes.get("/")
async def health():
    return {"status":"OK"}


@routes.get("/db")
async def check_database(db = Depends(get_db)):
    from sqlalchemy import text
    await db.execute(text("SELECT 1"))
    return {"status": "connected"}
