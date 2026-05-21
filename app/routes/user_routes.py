from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserCreationSchema, UserLoginSchema
from app.service import user_service
from app.db import get_db
from app.utils.security import get_current_user
routes = APIRouter(
    prefix="/users",
    tags=["Auth","User"],
)


@routes.post("/register")
async def register_user(user: UserCreationSchema, db: AsyncSession = Depends(get_db)):
    user_object = await user_service.save_user(user, db)
    return {"status":"created","user":user_object}


@routes.get("/all")
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all_user(db)


@routes.post("/login")
async def login_user(_body: UserLoginSchema, db: AsyncSession = Depends(get_db)):

    verified, token = await user_service.login(_body.email, _body.password, db)
    return {"message":"login","success": verified, "token": token}


@routes.get("/me")
async def me(user = Depends(get_current_user)):
    print("====---====")
    return user
