# Quiz Application

A comprehensive quiz web application built with FastAPI, PostgreSQL, and a modern admin dashboard. This application provides both API endpoints for mobile applications and a web-based admin interface for managing quiz content.

## Features

- **Quiz Categories**: Countries, Animals, Programming, Cyber Security
- **Admin Dashboard**: Modern web interface for managing content
- **RESTful API**: Complete API for mobile applications
- **Authentication**: JWT-based authentication for admin users
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Modern UI**: Responsive design with beautiful gradients

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with Passlib
- **Frontend**: HTML, CSS, JavaScript
- **Templates**: Jinja2

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz-application
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**
   - Create a new database named `QuizDb`
   - Create a user `adminuser` with password `1234`
                 - Grant all privileges on `QuizDb` to `adminuser`

5. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://adminuser:1234@localhost:5432/QuizDb
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Initialize the database**
   ```bash
   python init_db.py
   ```

7. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## Default Admin Credentials

After running `init_db.py`, you'll have a default admin user:
- **Username**: admin
- **Password**: admin123

## API Documentation

Once the application is running, you can access:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Admin Dashboard**: http://localhost:8000/admin/dashboard
- **Admin Login**: http://localhost:8000/admin/login

## API Endpoints

### Authentication
- `POST /auth/token` - Login and get access token
- `POST /auth/register` - Register new admin user
- `GET /auth/me` - Get current user info

### Admin API (Protected)
- `GET /admin/categories/` - List all categories
- `POST /admin/categories/` - Create new category
- `GET /admin/categories/{id}` - Get category by ID
- `PUT /admin/categories/{id}` - Update category
- `DELETE /admin/categories/{id}` - Delete category

- `GET /admin/questions/` - List all questions
- `POST /admin/questions/` - Create new question
- `GET /admin/questions/{id}` - Get question by ID
- `PUT /admin/questions/{id}` - Update question
- `DELETE /admin/questions/{id}` - Delete question

- `GET /admin/users/` - List all admin users
- `POST /admin/users/` - Create new admin user

### Public Quiz API
- `GET /quiz/categories/` - Get all quiz categories
- `GET /quiz/questions/{category_id}` - Get questions for category
- `GET /quiz/random/{category_id}` - Get random questions for category
- `POST /quiz/submit/{category_id}` - Submit quiz answers and get results

## Database Schema

### Categories
- `id` (Primary Key)
- `name` (Unique)
- `description`
- `created_at`
- `updated_at`

### Questions
- `id` (Primary Key)
- `question_text`
- `option_a`, `option_b`, `option_c`, `option_d`
- `correct_answer` (A, B, C, or D)
- `explanation`
- `category_id` (Foreign Key)
- `created_at`
- `updated_at`

### Admin Users
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `hashed_password`
- `is_active`
- `created_at`
- `updated_at`

## Project Structure

```
quiz-application/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── database.py            # Database connection and session
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication utilities
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── routers/              # API route modules
│   ├── __init__.py
│   ├── admin.py          # Admin API routes
│   ├── quiz.py           # Public quiz API routes
│   ├── auth.py           # Authentication routes
│   └── admin_web.py      # Admin dashboard web routes
└── templates/            # HTML templates
    ├── admin_login.html   # Admin login page
    └── admin_dashboard.html # Admin dashboard
```

## Usage Examples

### Creating a Category
```bash
curl -X POST "http://localhost:8000/admin/categories/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Science", "description": "Scientific knowledge questions"}'
```

### Adding a Question
```bash
curl -X POST "http://localhost:8000/admin/questions/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "What is the chemical symbol for gold?",
    "option_a": "Ag",
    "option_b": "Au",
    "option_c": "Fe",
    "option_d": "Cu",
    "correct_answer": "B",
    "explanation": "Au comes from the Latin word for gold, aurum.",
    "category_id": 1
  }'
```

### Taking a Quiz
```bash
# Get questions for a category
curl "http://localhost:8000/quiz/questions/1?limit=5"

# Submit answers
curl -X POST "http://localhost:8000/quiz/submit/1" \
  -H "Content-Type: application/json" \
  -d '[
    {"question_id": 1, "selected_answer": "B"},
    {"question_id": 2, "selected_answer": "A"}
  ]'
```

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
The application uses SQLAlchemy's `create_all()` for simplicity. For production, consider using Alembic for database migrations.

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (change in production)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Security Considerations

1. **Change default credentials**: Update the default admin password
2. **Secure SECRET_KEY**: Use a strong, random secret key in production
3. **Database security**: Use strong passwords and limit database access
4. **HTTPS**: Use HTTPS in production
5. **CORS**: Configure CORS properly for your domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository. 