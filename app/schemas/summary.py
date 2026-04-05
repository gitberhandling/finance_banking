"""Pydantic schemas for summary/analytics endpoints."""
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class AmountResponse(BaseModel):
    """Generic single-value response for totals."""

    total: Decimal


class CategorySummary(BaseModel):
    """Per-category aggregated amount."""

    category: str
    total: Decimal


class MonthlySummary(BaseModel):
    """Monthly aggregated income and expense."""

    year: int
    month: int
    income: Decimal
    expense: Decimal
    net: Decimal


class CategoryWiseResponse(BaseModel):
    data: List[CategorySummary]


class MonthlyTrendsResponse(BaseModel):
    data: List[MonthlySummary]
