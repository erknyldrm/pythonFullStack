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


# Enhanced Admin Registration schemas
class AdminUserCreateEnhanced(AdminUserBase):
    password: str
    confirm_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "admin"  # admin, super_admin, moderator


class AdminInvitation(BaseModel):
    email: str
    role: str = "admin"
    invited_by: Optional[int] = None


class AdminInvitationResponse(BaseModel):
    invitation_id: str
    email: str
    role: str
    expires_at: datetime
    invited_by: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    token: str
    new_password: str
    confirm_password: str


class EmailVerification(BaseModel):
    token: str


class AdminRegistrationResponse(BaseModel):
    user: AdminUser
    message: str
    requires_email_verification: bool = False


class AdminUserProfile(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


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