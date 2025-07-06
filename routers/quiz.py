from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category, Question
from schemas import QuizQuestion, QuizAnswer, QuizResult

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/categories/", response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    """Get all available quiz categories"""
    categories = db.query(Category).all()
    return [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "question_count": len(category.questions)
        }
        for category in categories
    ]


@router.get("/questions/{category_id}", response_model=List[QuizQuestion])
def get_quiz_questions(
    category_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get quiz questions for a specific category"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get questions for the category
    questions = db.query(Question).filter(Question.category_id == category_id).limit(limit).all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this category")
    
    # Convert to quiz format (without correct answer)
    quiz_questions = []
    for question in questions:
        quiz_questions.append(QuizQuestion(
            id=question.id,
            question_text=question.question_text,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            category_name=category.name
        ))
    
    return quiz_questions


@router.post("/submit/{category_id}", response_model=QuizResult)
def submit_quiz(
    category_id: int,
    answers: List[QuizAnswer],
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get results"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get all questions for the category
    questions = db.query(Question).filter(Question.category_id == category_id).all()
    question_dict = {q.id: q for q in questions}
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this category")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(answers)
    
    for answer in answers:
        question = question_dict.get(answer.question_id)
        if question and answer.selected_answer.upper() == question.correct_answer:
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    return QuizResult(
        total_questions=total_questions,
        correct_answers=correct_answers,
        score_percentage=round(score_percentage, 2),
        category_name=category.name
    )


@router.get("/random/{category_id}", response_model=List[QuizQuestion])
def get_random_questions(
    category_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get random questions for a specific category"""
    from sqlalchemy import func
    
    # Verify category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get random questions for the category
    questions = db.query(Question).filter(
        Question.category_id == category_id
    ).order_by(func.random()).limit(limit).all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this category")
    
    # Convert to quiz format
    quiz_questions = []
    for question in questions:
        quiz_questions.append(QuizQuestion(
            id=question.id,
            question_text=question.question_text,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            category_name=category.name
        ))
    
    return quiz_questions 