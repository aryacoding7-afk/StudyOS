import logging

from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    UsernameAlreadyExistsException,
)
from app.modules.auth.jwt import create_access_token
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import LoginRequest, UserCreate
from app.modules.auth.security import (
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)

    def register_user(
        self,
        user: UserCreate,
    ):
        logger.info(
            "Registering user with email '%s'",
            user.email,
        )

        if self.repository.get_by_email(user.email):
            logger.warning(
                "Registration failed: email '%s' already exists",
                user.email,
            )
            raise EmailAlreadyExistsException()

        if self.repository.get_by_username(user.username):
            logger.warning(
                "Registration failed: username '%s' already exists",
                user.username,
            )
            raise UsernameAlreadyExistsException()

        hashed_password = hash_password(user.password)

        created_user = self.repository.create_user(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        logger.info(
            "User %s registered successfully",
            created_user.id,
        )

        return created_user

    def login_user(
        self,
        user: LoginRequest,
    ):
        logger.info(
            "Login attempt for '%s'",
            user.email,
        )

        db_user = self.repository.get_by_email(user.email)

        if db_user is None:
            logger.warning(
                "Login failed for '%s': user not found",
                user.email,
            )
            raise InvalidCredentialsException()

        if not verify_password(
            user.password,
            db_user.hashed_password,
        ):
            logger.warning(
                "Login failed for '%s': invalid password",
                user.email,
            )
            raise InvalidCredentialsException()

        token = create_access_token(
            {
                "sub": str(db_user.id),
            }
        )

        logger.info(
            "User %s logged in successfully",
            db_user.id,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }