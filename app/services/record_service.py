"""Financial record service — CRUD with ownership enforcement."""
import logging
import uuid
from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial_record import FinancialRecord
from app.models.user import User
from app.repositories.record_repository import record_repository
from app.schemas.financial_record import RecordCreate, RecordUpdate

logger = logging.getLogger(__name__)


class RecordService:
    """Business logic for financial record CRUD."""

    async def create_record(
        self,
        db: AsyncSession,
        payload: RecordCreate,
        current_user: User,
    ) -> FinancialRecord:
        """Create a new financial record for the authenticated user."""
        obj_data = {
            "user_id": current_user.id,
            "amount": payload.amount,
            "type": payload.type,
            "category": payload.category,
            "date": payload.date,
            "notes": payload.notes,
        }
        record = await record_repository.create(db, obj_data)
        logger.info("Record created: %s (user=%s)", record.id, current_user.id)
        return record

    async def get_records(
        self,
        db: AsyncSession,
        current_user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None,
        record_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[FinancialRecord]:
        """Return the current user's records with optional filters."""
        return await record_repository.get_by_user(
            db,
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            category=category,
            record_type=record_type,
            skip=skip,
            limit=limit,
        )

    async def get_record(
        self,
        db: AsyncSession,
        record_id: uuid.UUID,
        current_user: User,
    ) -> FinancialRecord:
        """Return a single record (must belong to current user)."""
        record = await record_repository.get_user_record(db, record_id, current_user.id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        return record

    async def update_record(
        self,
        db: AsyncSession,
        record_id: uuid.UUID,
        payload: RecordUpdate,
        current_user: User,
    ) -> FinancialRecord:
        """Update a record (must belong to current user)."""
        record = await self.get_record(db, record_id, current_user)
        update_data = payload.model_dump(exclude_unset=True)
        return await record_repository.update(db, record, update_data)

    async def delete_record(
        self,
        db: AsyncSession,
        record_id: uuid.UUID,
        current_user: User,
    ) -> None:
        """Delete a record (must belong to current user)."""
        record = await self.get_record(db, record_id, current_user)
        await db.delete(record)


record_service = RecordService()
