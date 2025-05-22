from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..models.post import PostCreate, Post, PostUpdate
from ..services.post import (
    create_post,
    get_post,
    update_post,
    delete_post,
    get_all_posts
)

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=Post, status_code=201)
async def create_blog_post(post: PostCreate):
    return await create_post(post)

@router.get("/{post_id}", response_model=Post)
async def get_blog_post(post_id: str):
    return await get_post(post_id)

@router.patch("/{post_id}", response_model=Post)
async def update_blog_post(post_id: str, post_update: PostUpdate):
    return await update_post(post_id, post_update)

@router.delete("/{post_id}", status_code=204)
async def delete_blog_post(post_id: str):
    deleted = await delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    
@router.get("", response_model=List[Post])
async def get_blog_posts(
    search_term: Optional[str] = Query(None, description="Search term for filtering posts"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return await get_all_posts(search_term, skip, limit)