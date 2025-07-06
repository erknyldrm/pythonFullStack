from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers import admin, quiz, auth, admin_web

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiz Application API",
    description="A comprehensive quiz application with admin dashboard and public quiz functionality",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(quiz.router)
app.include_router(admin_web.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Quiz Application API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
