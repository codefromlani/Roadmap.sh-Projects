from pydantic import BaseModel, ConfigDict
import enum
from typing import Optional
from datetime import datetime


class ExpenseCategory(enum.Enum):
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilities"
    CLOTHING = "clothing"
    HEALTH = "health"
    OTHERS = "others"

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: ExpenseCategory
    date: Optional[datetime] = None

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[ExpenseCategory] = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str
    category: ExpenseCategory
    date: datetime

    model_config = ConfigDict(
        from_attributes=True
    )