from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate
from app.modules.auth.security import hash_password


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