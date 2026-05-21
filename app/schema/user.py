from datetime import datetime
from pydantic import BaseModel


class UserCore(BaseModel):
    email: str
    password: str


class UserLoginSchema(UserCore):
    pass


class UserBase(UserCore):
    full_name: str


class UserCreationSchema(UserBase):
    confirm_password: str


class User(UserBase):
    email_verified: bool
    is_active: bool
    created_at: datetime
    
