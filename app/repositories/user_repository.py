"""User data-access repository."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Extends BaseRepository with user-specific queries."""

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Return a user matching the given email, or None."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()


user_repository = UserRepository(User)
