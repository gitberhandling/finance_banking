"""Pydantic schemas for FinancialRecord."""
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    """Payload to create a financial record."""

    amount: Decimal = Field(..., gt=0, decimal_places=2)
    type: Literal["income", "expense"]
    category: str = Field(..., min_length=1, max_length=100)
    date: date
    notes: Optional[str] = None


class RecordUpdate(BaseModel):
    """Payload to partially update a financial record."""

    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[date] = None
    notes: Optional[str] = None


class RecordOut(BaseModel):
    """Response schema for a financial record."""

    id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    type: str
    category: str
    date: date
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RecordFilters(BaseModel):
    """Optional query-param filters for listing records."""

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category: Optional[str] = None
    type: Optional[Literal["income", "expense"]] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=200)
