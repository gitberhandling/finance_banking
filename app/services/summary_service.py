"""Summary analytics service — aggregations over financial records."""
import logging
import uuid
from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial_record import FinancialRecord
from app.models.user import User
from app.schemas.summary import (
    AmountResponse,
    CategorySummary,
    MonthlySummary,
)

logger = logging.getLogger(__name__)


class SummaryService:
    """Async aggregation queries for financial analytics."""

    def _base_query(
        self,
        user_id: uuid.UUID,
        start_date: Optional[date],
        end_date: Optional[date],
    ):
        """Build a base filtered select on FinancialRecord."""
        q = select(FinancialRecord).where(
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted == False,
        )
        if start_date:
            q = q.where(FinancialRecord.date >= start_date)
        if end_date:
            q = q.where(FinancialRecord.date <= end_date)
        return q

    async def _sum_by_type(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        record_type: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Decimal:
        """Return aggregate SUM for a given record type."""
        query = (
            select(func.coalesce(func.sum(FinancialRecord.amount), 0))
            .where(FinancialRecord.user_id == user_id)
            .where(FinancialRecord.type == record_type)
            .where(FinancialRecord.is_deleted == False)
        )
        if start_date:
            query = query.where(FinancialRecord.date >= start_date)
        if end_date:
            query = query.where(FinancialRecord.date <= end_date)

        result = await db.execute(query)
        return result.scalar() or Decimal("0")

    async def total_income(
        self,
        db: AsyncSession,
        current_user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> AmountResponse:
        total = await self._sum_by_type(db, current_user.id, "income", start_date, end_date)
        return AmountResponse(total=total)

    async def total_expense(
        self,
        db: AsyncSession,
        current_user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> AmountResponse:
        total = await self._sum_by_type(db, current_user.id, "expense", start_date, end_date)
        return AmountResponse(total=total)

    async def net_balance(
        self,
        db: AsyncSession,
        current_user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> AmountResponse:
        income = await self._sum_by_type(db, current_user.id, "income", start_date, end_date)
        expense = await self._sum_by_type(db, current_user.id, "expense", start_date, end_date)
        return AmountResponse(total=income - expense)

    async def category_wise(
        self,
        db: AsyncSession,
        current_user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[CategorySummary]:
        """Return total per category (income + expense combined)."""
        query = (
            select(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount).label("total"),
            )
            .where(FinancialRecord.user_id == current_user.id)
            .where(FinancialRecord.is_deleted == False)
            .group_by(FinancialRecord.category)
            .order_by(func.sum(FinancialRecord.amount).desc())
        )
        if start_date:
            query = query.where(FinancialRecord.date >= start_date)
        if end_date:
            query = query.where(FinancialRecord.date <= end_date)

        result = await db.execute(query)
        return [CategorySummary(category=row.category, total=row.total) for row in result.all()]

    async def monthly_trends(
        self,
        db: AsyncSession,
        current_user: User,
    ) -> List[MonthlySummary]:
        """Return month-by-month income, expense, and net balance."""
        income_q = (
            select(
                func.extract("year", FinancialRecord.date).label("year"),
                func.extract("month", FinancialRecord.date).label("month"),
                func.sum(FinancialRecord.amount).label("income"),
            )
            .where(FinancialRecord.user_id == current_user.id)
            .where(FinancialRecord.type == "income")
            .where(FinancialRecord.is_deleted == False)
            .group_by("year", "month")
        )
        expense_q = (
            select(
                func.extract("year", FinancialRecord.date).label("year"),
                func.extract("month", FinancialRecord.date).label("month"),
                func.sum(FinancialRecord.amount).label("expense"),
            )
            .where(FinancialRecord.user_id == current_user.id)
            .where(FinancialRecord.type == "expense")
            .where(FinancialRecord.is_deleted == False)
            .group_by("year", "month")
        )

        inc_result = {
            (int(r.year), int(r.month)): r.income
            for r in (await db.execute(income_q)).all()
        }
        exp_result = {
            (int(r.year), int(r.month)): r.expense
            for r in (await db.execute(expense_q)).all()
        }

        all_keys = sorted(set(inc_result) | set(exp_result))
        return [
            MonthlySummary(
                year=y,
                month=m,
                income=inc_result.get((y, m), Decimal("0")),
                expense=exp_result.get((y, m), Decimal("0")),
                net=inc_result.get((y, m), Decimal("0")) - exp_result.get((y, m), Decimal("0")),
            )
            for y, m in all_keys
        ]


summary_service = SummaryService()
