"""Pydantic schemas for User."""
import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload to create a new user (public registration)."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["viewer", "analyst", "admin"] = "viewer"


class UserUpdate(BaseModel):
    """Payload to partially update a user."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    status: Optional[Literal["active", "inactive"]] = None


class UserOut(BaseModel):
    """Response schema — never exposes hashed_password."""

    id: uuid.UUID
    name: str
    email: EmailStr
    role: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
