from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate
from app.modules.auth.security import hash_password

from app.modules.auth.jwt import create_access_token
from app.modules.auth.security import verify_password
from app.modules.auth.schemas import LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)

    def register_user(self, user: UserCreate):
        # Check if email already exists
        if self.repository.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username already exists
        if self.repository.get_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Hash the password
        hashed_password = hash_password(user.password)

        # Save user
        return self.repository.create_user(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
    def login_user(self, user: LoginRequest):
        db_user = self.repository.get_by_email(user.email)

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": str(db_user.id),
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
    