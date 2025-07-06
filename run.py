#!/usr/bin/env python3
"""
Quiz Application Startup Script

This script starts the FastAPI application with proper configuration.
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI application"""
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import fastapi
        import sqlalchemy
        import psycopg2
    except ImportError as e:
        print(f"❌ Error: Missing dependencies. Please install requirements first:")
        print("   pip install -r requirements.txt")
        print(f"   Missing: {e}")
        sys.exit(1)
    
    print("🚀 Starting Quiz Application...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🎯 Public Quiz: http://localhost:8000/")
    print("⚙️  Admin Dashboard: http://localhost:8000/admin/dashboard")
    print("🔐 Admin Login: http://localhost:8000/admin/login")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 