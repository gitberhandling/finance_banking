"""User management service."""
import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserOut, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    """Business logic for user CRUD operations."""

    async def create_user(
        self,
        db: AsyncSession,
        payload: UserCreate,
    ) -> User:
        """Admin-facing user creation (can set role explicitly)."""
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
            "role": payload.role,
            "status": "active",
        }
        return await user_repository.create(db, obj_data)

    async def get_all_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
    ) -> List[User]:
        """Return paginated list of all users (admin only)."""
        return await user_repository.get_multi(db, skip=skip, limit=limit)

    async def update_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        payload: UserUpdate,
        current_user: User,
    ) -> User:
        """Update user — users can only update themselves, admins can update any."""
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        db_user = await user_repository.get(db, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        update_data = payload.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        return await user_repository.update(db, db_user, update_data)

    async def delete_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        current_user: User,
    ) -> None:
        """Delete a user — admins only."""
        if current_user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        deleted = await user_repository.delete(db, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


user_service = UserService()
