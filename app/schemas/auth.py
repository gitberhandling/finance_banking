"""Pydantic schemas for Auth endpoints."""
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Payload for POST /auth/login."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    """Payload for POST /auth/register."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
