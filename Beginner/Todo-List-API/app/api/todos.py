from fastapi import APIRouter, HTTPException, Depends, status,Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional

from ..schemas.todo import TodoResponse, TodoCreate, TodoListResponse, TodoUpdate
from ..db.database import get_db
from ..db.models import User, Todo
from ..core.security import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("", response_model=TodoResponse)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

@router.get("", response_model=TodoListResponse)
async def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Todo.title.ilike(search_filter)) |
            (Todo.description.ilike(search_filter))
        )

    total = query.count()

    offset = (page - 1) * limit
    todos = query.offset(offset).limit(limit).all()

    return TodoListResponse(
        data=todos,
        page=page,
        limit=limit,
        total=total
    )

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if not db_todo:
        # Check if todo exists but belongs to another user
        other_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if other_todo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db_todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not db_todo:
        other_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if other_todo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
    
    db.delete(db_todo)
    db.commit()
