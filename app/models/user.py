"""User SQLAlchemy model."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """Users table — stores credentials, role, and status."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), nullable=False, default="viewer")   # "viewer" | "analyst" | "admin"
    status = Column(String(50), nullable=False, default="active")  # "active" | "inactive"
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # One-to-many: a user owns many financial records
    records = relationship("FinancialRecord", back_populates="owner", cascade="all, delete-orphan")
