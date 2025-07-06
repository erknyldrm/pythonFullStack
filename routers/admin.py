from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category, Question, AdminUser
from schemas import (
    CategoryCreate, CategoryUpdate, Category as CategorySchema,
    QuestionCreate, QuestionUpdate, Question as QuestionSchema,
    AdminUserCreate, AdminUserUpdate, AdminUser as AdminUserSchema
)
from auth import get_current_active_user, get_password_hash

router = APIRouter(prefix="/admin", tags=["admin"])


# Category endpoints
@router.post("/categories/", response_model=CategorySchema)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/", response_model=List[CategorySchema])
def get_categories(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    return db.query(Category).all()


@router.get("/categories/{category_id}", response_model=CategorySchema)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}


# Question endpoints
@router.post("/questions/", response_model=QuestionSchema)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    # Validate category exists
    category = db.query(Category).filter(Category.id == question.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate correct answer format
    if question.correct_answer not in ['A', 'B', 'C', 'D']:
        raise HTTPException(status_code=400, detail="Correct answer must be A, B, C, or D")
    
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/questions/", response_model=List[QuestionSchema])
def get_questions(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    query = db.query(Question)
    if category_id:
        query = query.filter(Question.category_id == category_id)
    return query.offset(skip).limit(limit).all()


@router.get("/questions/{question_id}", response_model=QuestionSchema)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_update.dict(exclude_unset=True)
    
    # Validate correct answer if provided
    if 'correct_answer' in update_data and update_data['correct_answer'] not in ['A', 'B', 'C', 'D']:
        raise HTTPException(status_code=400, detail="Correct answer must be A, B, C, or D")
    
    # Validate category if provided
    if 'category_id' in update_data:
        category = db.query(Category).filter(Category.id == update_data['category_id']).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}


# Admin user endpoints
@router.post("/users/", response_model=AdminUserSchema)
def create_admin_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    # Check if username already exists
    existing_user = db.query(AdminUser).filter(AdminUser.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(AdminUser).filter(AdminUser.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = AdminUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[AdminUserSchema])
def get_admin_users(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    return db.query(AdminUser).all() 