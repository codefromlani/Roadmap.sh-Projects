from sqlalchemy import String, Integer, Column, DateTime, Float, Enum, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum

from ..database import Base

class ExpenseCategory(enum.Enum):
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilities"
    CLOTHING = "clothing"
    HEALTH = "health"
    OTHERS = "others"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    category = Column(Enum(ExpenseCategory), nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="expenses")