from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
import re

from ..models.post import PostCreate, Post, PostUpdate
from ..database import posts_collection

async def create_post(post: PostCreate) -> Post:
    post_data = post.model_dump()
    post_data["_id"] = str(ObjectId())  
    post_data["created_at"] = datetime.utcnow()
    post_data["updated_at"] = datetime.utcnow()

    await posts_collection.insert_one(post_data)
    return Post(**post_data)

async def get_post(post_id: str) -> Optional[Post]:
    post = await posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return Post(**post)

async def update_post(post_id: str, post_update: PostUpdate) -> Optional[Post]:
    existing_post = await get_post(post_id)
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    update_data = {k: v for k, v in post_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    await posts_collection.update_one(
        {"_id": post_id},
        {"$set": update_data}
    )
    return await get_post(post_id)

async def delete_post(post_id: str) -> bool:
    result = await posts_collection.delete_one({"_id": post_id})
    return result.deleted_count > 0

async def get_all_posts(
        search_term: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Post]:
    query = {}

    if search_term:
        # Case-insensitive search across title, content, and category
        search_pattern = re.compile(search_term, re.IGNORECASE)
        query = {
            "$or": [
                {"title": {"$regex": search_pattern}},
                {"content": {"$regex": search_pattern}},
                {"category": {"$regex": search_pattern}}
            ]
        }

    cursor = posts_collection.find(query).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    return [Post(**post) for post in posts]