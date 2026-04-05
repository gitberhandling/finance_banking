"""User management endpoints."""
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_role
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Create user (admin)")
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Admin-only: create a user with an explicit role."""
    return await user_service.create_user(db, payload)


@router.get("/", response_model=List[UserOut], summary="List all users (admin)")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Admin-only: paginated list of all users."""
    return await user_service.get_all_users(db, skip=skip, limit=limit)


@router.get("/me", response_model=UserOut, summary="Get current user profile")
async def get_me(current_user: User = Depends(get_current_user)):
    """Return the authenticated user's own profile."""
    return current_user


@router.patch("/{user_id}", response_model=UserOut, summary="Update a user")
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Users can update themselves; admins can update any user."""
    return await user_service.update_user(db, user_id, payload, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user (admin)")
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Admin-only: permanently delete a user."""
    await user_service.delete_user(db, user_id, current_user)
