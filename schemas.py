from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Question schemas
class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: Optional[str] = None
    category_id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    category_id: Optional[int] = None


class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    
    class Config:
        from_attributes = True


# Admin User schemas
class AdminUserBase(BaseModel):
    username: str
    email: str


class AdminUserCreate(AdminUserBase):
    password: str


class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class AdminUser(AdminUserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Quiz schemas
class QuizQuestion(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    category_name: str
    
    class Config:
        from_attributes = True


class QuizAnswer(BaseModel):
    question_id: int
    selected_answer: str


class QuizResult(BaseModel):
    total_questions: int
    correct_answers: int
    score_percentage: float
    category_name: str 