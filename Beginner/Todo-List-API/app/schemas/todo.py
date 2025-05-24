from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class TodoListResponse(BaseModel):
    data: List[TodoResponse]
    page: int
    limit: int
    total: int