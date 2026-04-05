"""Financial records endpoints with full CRUD + query filter support."""
import uuid
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_role
from app.core.database import get_db
from app.models.user import User
from app.schemas.financial_record import RecordCreate, RecordOut, RecordUpdate
from app.services.record_service import record_service

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordOut, status_code=status.HTTP_201_CREATED, summary="Create a financial record")
async def create_record(
    payload: RecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Create a new income or expense record for the authenticated user."""
    return await record_service.create_record(db, payload, current_user)


@router.get("/", response_model=List[RecordOut], summary="List records with optional filters")
async def list_records(
    start_date: Optional[date] = Query(None, description="Filter from this date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter up to this date (inclusive)"),
    category: Optional[str] = Query(None, description="Filter by category name"),
    type: Optional[str] = Query(None, description="Filter by type: income | expense"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["analyst", "admin"])),
):
    """Return the current user's records, optionally filtered by date range, category, or type."""
    return await record_service.get_records(
        db,
        current_user,
        start_date=start_date,
        end_date=end_date,
        category=category,
        record_type=type,
        skip=skip,
        limit=limit,
    )


@router.get("/{record_id}", response_model=RecordOut, summary="Get a specific record")
async def get_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["analyst", "admin"])),
):
    """Return a single financial record by ID (must belong to the authenticated user)."""
    return await record_service.get_record(db, record_id, current_user)


@router.patch("/{record_id}", response_model=RecordOut, summary="Update a record")
async def update_record(
    record_id: uuid.UUID,
    payload: RecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Partially update a financial record."""
    return await record_service.update_record(db, record_id, payload, current_user)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a record")
async def delete_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Delete a financial record."""
    await record_service.delete_record(db, record_id, current_user)
