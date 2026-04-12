from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    nickname: Optional[str]
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    sort_order: int
    owner_id: int
    created_at: datetime


# ── Bookmark ──────────────────────────────────────────────────────────────────

class BookmarkCreate(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    favicon_url: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: int = 0


class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    favicon_url: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: Optional[int] = None


class BookmarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    url: str
    description: Optional[str]
    favicon_url: Optional[str]
    sort_order: int
    category_id: Optional[int]
    owner_id: int
    created_at: datetime
    updated_at: datetime
