from sqlalchemy import String, Integer, Column, DateTime, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")