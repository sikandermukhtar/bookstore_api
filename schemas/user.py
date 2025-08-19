from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserRead(BaseModel):
    id: UUID
    role: str
    email: EmailStr
    profile_img_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    role: str


class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(...)


class UserLoginSuccess(BaseModel):
    user: UserRead
    message: str
    access_token: str
    token_type: str


class UserDelete(BaseModel):
    user: UserRead
    message: str
