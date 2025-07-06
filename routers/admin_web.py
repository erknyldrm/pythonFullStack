from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(prefix="/admin", tags=["admin-web"])

# Set up templates
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    """Serve the admin login page"""
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Serve the admin dashboard page"""
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def public_quiz(request: Request):
    """Serve the public quiz interface"""
    return templates.TemplateResponse("quiz.html", {"request": request}) 