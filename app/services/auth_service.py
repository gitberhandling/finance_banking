"""Auth service — registration and login business logic."""
import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import user_repository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


class AuthService:
    """Handles user registration and token-based login."""

    async def register(
        self,
        db: AsyncSession,
        payload: RegisterRequest,
    ) -> dict:
        """Register a new user.

        Raises:
            HTTPException 409 if email already registered.
        """
        existing = await user_repository.get_by_email(db, payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered.",
            )

        obj_data = {
            "name": payload.name,
            "email": payload.email,
            "hashed_password": get_password_hash(payload.password),
            "role": "viewer",
            "status": "active",
        }
        user = await user_repository.create(db, obj_data)
        logger.info("New user registered: %s", user.email)
        return {"message": "Registration successful", "user_id": str(user.id)}

    async def login(
        self,
        db: AsyncSession,
        email: str,
        password: str,
    ) -> TokenResponse:
        """Authenticate user and return JWT token.

        Raises:
            HTTPException 401 for invalid credentials.
        """
        user = await user_repository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive.",
            )

        token = create_access_token({"sub": str(user.id), "role": user.role})
        logger.info("User logged in: %s", user.email)
        return TokenResponse(access_token=token)


auth_service = AuthService()
