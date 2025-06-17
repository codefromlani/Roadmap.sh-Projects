from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List

from ..db.models.user import User
from ..db.models.expense import Expense
from ..db.database import get_db
from ..schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from ..core.security import get_current_user


router = APIRouter(tags=["expenses"])

@router.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        category=expense.category,
        date=expense.date or datetime.utcnow(),
        user_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(
    filter_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    if filter_type:
        now = datetime.utcnow()
        if filter_type == "week":
            start_date = now - timedelta(days=7)
        elif filter_type == "month":
            start_date = now - timedelta(days=30)
        elif filter_type == "3months":
            start_date = now - timedelta(days=90)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
    
    if start_date and end_date:
        query = query.filter(Expense.date >= start_date, Expense.date <= end_date)
    
    return query.order_by(Expense.date.desc()).all()

@router.patch("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Expense not found"
        )
    
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Expense not found"
        )
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}