from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from app.utils import hash_password, verify_password,create_access_token
from app.schema import UserCreationSchema
from app.models import User


async def save_user(user_schema: UserCreationSchema, db: AsyncSession):

    if user_schema.password != user_schema.confirm_password:
        raise HTTPException(status_code=400, detail="Password didn't match.")
    
    user = await get_user_by_email(user_schema.email, db)
    if user:
        raise HTTPException(status_code=400, detail="Email already Exist.")

    user_schema.password = hash_password(user_schema.password)
    obj = user_schema.model_dump()
    obj.pop("confirm_password")
    print(obj)
    user = User(**(obj))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_all_user(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result if result else list()


async def get_user_by_email(email, db):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user

async def login(email: str, password: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=400, detail="Email or Password is incorrect.")
    
    if verify_password(password, user.password):
        auth = {"id":user.id}
        token = create_access_token(auth)
        print(token)
        return True, token
    
    return False, None
