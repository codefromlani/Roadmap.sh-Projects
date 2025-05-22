from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class Post(PostBase):
    id: Optional[str] = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders = {ObjectId: str}
    )
