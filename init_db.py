from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Category, Question, AdminUser
from auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()
    try:
        # Check if categories already exist
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("Database already initialized. Skipping...")
            return
        
        # Create initial categories
        categories = [
            Category(name="Countries", description="Test your knowledge about countries around the world"),
            Category(name="Animals", description="Learn about different animal species and their characteristics"),
            Category(name="Programming", description="Challenge yourself with programming concepts and languages"),
            Category(name="Cyber Security", description="Test your knowledge about cybersecurity and digital safety")
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # Create sample questions for each category
        sample_questions = [
            # Countries
            {
                "question_text": "What is the capital of France?",
                "option_a": "London",
                "option_b": "Paris",
                "option_c": "Berlin",
                "option_d": "Madrid",
                "correct_answer": "B",
                "explanation": "Paris is the capital and largest city of France.",
                "category_id": 1
            },
            {
                "question_text": "Which country is known as the Land of the Rising Sun?",
                "option_a": "China",
                "option_b": "Korea",
                "option_c": "Japan",
                "option_d": "Thailand",
                "correct_answer": "C",
                "explanation": "Japan is often called the Land of the Rising Sun due to its location east of the Asian mainland.",
                "category_id": 1
            },
            # Animals
            {
                "question_text": "What is the largest mammal in the world?",
                "option_a": "African Elephant",
                "option_b": "Blue Whale",
                "option_c": "Giraffe",
                "option_d": "Polar Bear",
                "correct_answer": "B",
                "explanation": "The Blue Whale is the largest mammal, reaching lengths of up to 100 feet.",
                "category_id": 2
            },
            {
                "question_text": "Which animal is known as the 'King of the Jungle'?",
                "option_a": "Tiger",
                "option_b": "Lion",
                "option_c": "Leopard",
                "option_d": "Cheetah",
                "correct_answer": "B",
                "explanation": "The Lion is often called the King of the Jungle, though they actually live in grasslands.",
                "category_id": 2
            },
            # Programming
            {
                "question_text": "What does HTML stand for?",
                "option_a": "Hyper Text Markup Language",
                "option_b": "High Tech Modern Language",
                "option_c": "Home Tool Markup Language",
                "option_d": "Hyperlink and Text Markup Language",
                "correct_answer": "A",
                "explanation": "HTML stands for Hyper Text Markup Language, the standard markup language for web pages.",
                "category_id": 3
            },
            {
                "question_text": "Which programming language is known as the 'language of the web'?",
                "option_a": "Python",
                "option_b": "Java",
                "option_c": "JavaScript",
                "option_d": "C++",
                "correct_answer": "C",
                "explanation": "JavaScript is often called the language of the web as it's essential for interactive web development.",
                "category_id": 3
            },
            # Cyber Security
            {
                "question_text": "What is a 'phishing' attack?",
                "option_a": "A type of virus",
                "option_b": "A fishing game",
                "option_c": "A fraudulent attempt to steal sensitive information",
                "option_d": "A type of firewall",
                "correct_answer": "C",
                "explanation": "Phishing is a cyber attack where attackers pose as legitimate entities to steal sensitive information.",
                "category_id": 4
            },
            {
                "question_text": "What does VPN stand for?",
                "option_a": "Virtual Private Network",
                "option_b": "Very Private Network",
                "option_c": "Virtual Public Network",
                "option_d": "Verified Private Network",
                "correct_answer": "A",
                "explanation": "VPN stands for Virtual Private Network, which provides secure, encrypted connections.",
                "category_id": 4
            }
        ]
        
        for question_data in sample_questions:
            question = Question(**question_data)
            db.add(question)
        
        # Create a default admin user
        admin_user = AdminUser(
            username="admin",
            email="admin@quizapp.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin_user)
        
        db.commit()
        print("Database initialized successfully!")
        print("Default admin credentials:")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db() 