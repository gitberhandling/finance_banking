"""FinancialRecord data-access repository with filtering support."""
import uuid
from datetime import date
from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial_record import FinancialRecord
from app.repositories.base_repository import BaseRepository


class RecordRepository(BaseRepository[FinancialRecord]):
    """Extends BaseRepository with record-specific filtered queries."""

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None,
        record_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[FinancialRecord]:
        """Return records for a user with optional date/category/type filters."""
        query = select(FinancialRecord).where(
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted == False,
        )

        if start_date:
            query = query.where(FinancialRecord.date >= start_date)
        if end_date:
            query = query.where(FinancialRecord.date <= end_date)
        if category:
            query = query.where(FinancialRecord.category == category)
        if record_type:
            query = query.where(FinancialRecord.type == record_type)

        query = query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_user_record(
        self,
        db: AsyncSession,
        record_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Optional[FinancialRecord]:
        """Return a record only if it belongs to the given user."""
        result = await db.execute(
            select(FinancialRecord).where(
                FinancialRecord.id == record_id,
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted == False,
            )
        )
        return result.scalars().first()


    async def delete(self, db: AsyncSession, id: object) -> bool:
        """Soft-delete a record by marking is_deleted = True."""
        obj = await self.get(db, id)
        if obj and not obj.is_deleted:
            obj.is_deleted = True
            db.add(obj)
            await db.flush()
            return True
        return False

record_repository = RecordRepository(FinancialRecord)
