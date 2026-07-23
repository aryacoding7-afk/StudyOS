from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.modules.auth.service import AuthService
from app.models.user import User
from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register_user(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.login_user(user)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user