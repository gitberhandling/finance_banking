"""Summary / analytics endpoints."""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_role
from app.core.database import get_db
from app.models.user import User
from app.schemas.summary import (
    AmountResponse,
    CategoryWiseResponse,
    MonthlyTrendsResponse,
)
from app.services.summary_service import summary_service

router = APIRouter(prefix="/summary", tags=["Summary"])

_date_params = {
    "start_date": Query(None, description="Optional start date filter"),
    "end_date": Query(None, description="Optional end date filter"),
}


@router.get("/total-income", response_model=AmountResponse, summary="Total income")
async def get_total_income(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    """Aggregate sum of all income records."""
    return await summary_service.total_income(db, current_user, start_date, end_date)


@router.get("/total-expense", response_model=AmountResponse, summary="Total expense")
async def get_total_expense(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    """Aggregate sum of all expense records."""
    return await summary_service.total_expense(db, current_user, start_date, end_date)


@router.get("/net-balance", response_model=AmountResponse, summary="Net balance (income – expense)")
async def get_net_balance(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    """Net balance = total income minus total expense."""
    return await summary_service.net_balance(db, current_user, start_date, end_date)


@router.get("/category-wise", response_model=CategoryWiseResponse, summary="Totals per category")
async def get_category_wise(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    """Per-category sum of all financial records."""
    data = await summary_service.category_wise(db, current_user, start_date, end_date)
    return CategoryWiseResponse(data=data)


@router.get("/monthly-trends", response_model=MonthlyTrendsResponse, summary="Monthly income & expense trends")
async def get_monthly_trends(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    """Month-by-month breakdown of income, expense, and net for all time."""
    data = await summary_service.monthly_trends(db, current_user)
    return MonthlyTrendsResponse(data=data)
