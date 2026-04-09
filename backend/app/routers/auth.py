import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.email import send_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    user = User(email=body.email, hashed_pw=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_pw):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已禁用")
    return {"access_token": create_access_token(user.id)}


@router.post("/forgot-password", status_code=200)
def forgot_password(
    body: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == body.email).first()
    if user and user.is_active:
        raw_token = secrets.token_urlsafe(32)
        user.reset_token = _sha256(raw_token)
        user.reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        db.commit()
        background_tasks.add_task(send_reset_email, user.email, raw_token)
    return {"message": "如果该邮箱已注册，您将收到重置邮件"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/change-password", status_code=200)
def change_password(
    body: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(body.old_password, current_user.hashed_pw):
        raise HTTPException(status_code=400, detail="当前密码错误")
    if len(body.new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码至少6位")
    current_user.hashed_pw = hash_password(body.new_password)
    db.commit()
    return {"message": "密码已修改"}


@router.post("/reset-password", status_code=200)
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = _sha256(body.token)
    user = db.query(User).filter(User.reset_token == token_hash).first()
    if not user:
        raise HTTPException(status_code=400, detail="无效或已过期的重置链接")
    if user.reset_expires is None or user.reset_expires.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="重置链接已过期")
    user.hashed_pw = hash_password(body.new_password)
    user.reset_token = None
    user.reset_expires = None
    db.commit()
    return {"message": "密码已重置，请重新登录"}
