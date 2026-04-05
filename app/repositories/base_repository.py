"""Generic async CRUD base repository."""
from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Provides standard get/list/create/update/delete for any SQLAlchemy model."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Return a single record by primary key."""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Return paginated list of all records."""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_data: dict) -> ModelType:
        """Create a new record from a plain dict."""
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        update_data: dict,
    ) -> ModelType:
        """Apply partial updates to an existing record."""
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: Any) -> bool:
        """Delete a record by primary key. Returns True if found and deleted."""
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            return True
        return False
