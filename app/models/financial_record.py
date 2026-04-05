"""FinancialRecord SQLAlchemy model."""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class FinancialRecord(Base):
    """Financial records table — tracks income/expense transactions."""

    __tablename__ = "financial_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount = Column(Numeric(15, 2), nullable=False)
    type = Column(String(50), nullable=False)       # "income" | "expense"
    category = Column(String(100), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    notes = Column(Text, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    owner = relationship("User", back_populates="records")

    # Composite indexes for common query patterns
    __table_args__ = (
        Index("ix_financial_records_user_id", "user_id"),
        Index("ix_financial_records_date", "date"),
        Index("ix_financial_records_category", "category"),
    )
