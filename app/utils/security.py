import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy import Select

from app.models import User
from app.db import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXP_MIN = os.getenv("ACCESS_TOKEN_EXP_MIN", 15)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = HTTPBearer()

import bcrypt
bcrypt.__about__ = bcrypt

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXP_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(oauth_scheme),
        db = Depends(get_db)
    ):
    credential_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please provide correct credentials.",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        token = creds.credentials
        print("TOKEN :", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id = payload.get("id")
        if id is None:
            raise credential_exp
    except JWTError:
        raise credential_exp
    
    user = await get_user_by_id(id=id, db=db)
    print(user)
    if user is None:
        raise credential_exp
    return user

async def get_user_by_id(id, db):
    stmt = Select(User).where(User.id == id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user