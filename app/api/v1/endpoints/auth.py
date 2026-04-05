"""Auth endpoints: register and login."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201, summary="Register a new user")
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user account and return confirmation."""
    return await auth_service.register(db, payload)


@router.post("/login", response_model=TokenResponse, summary="Login and get JWT token")
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate with email/password and receive a Bearer token."""
    return await auth_service.login(db, payload.email, payload.password)
