from sqlalchemy import String, Integer, Column, DateTime, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    expenses = relationship("Expense", back_populates="owner")