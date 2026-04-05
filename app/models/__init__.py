# app/models package — import all models here so Alembic can discover them
from app.models.user import User
from app.models.financial_record import FinancialRecord

__all__ = ["User", "FinancialRecord"]
