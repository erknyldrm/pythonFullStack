#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Quiz Application

This script helps you set up the PostgreSQL database and user for the quiz application.
Run this script as a PostgreSQL superuser (usually postgres).
"""

import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_database():
    """Set up the database and user for the quiz application"""
    
    # Database configuration
    DB_NAME = "QuizDb"
    DB_USER = "adminuser"
    DB_PASSWORD = "1234"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    try:
        # Connect to PostgreSQL as superuser
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="postgres",  # Default superuser
            password="",      # You may need to set this
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user already exists
        print("Checking if user exists...")
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (DB_USER,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"Creating user '{DB_USER}'...")
            cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}'")
            print(f"User '{DB_USER}' created successfully!")
        else:
            print(f"User '{DB_USER}' already exists.")
        
        # Check if database already exists
        print("Checking if database exists...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"Creating database '{DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        cursor.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER}")
        cursor.execute(f"ALTER USER {DB_USER} CREATEDB")
        print("Privileges granted successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n✅ PostgreSQL setup completed successfully!")
        print(f"Database: {DB_NAME}")
        print(f"User: {DB_USER}")
        print(f"Password: {DB_PASSWORD}")
        print(f"Connection URL: postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("\nMake sure PostgreSQL is running and you have the correct credentials.")
        print("You may need to:")
        print("1. Start PostgreSQL service")
        print("2. Set the correct password for the postgres user")
        print("3. Run this script as the postgres user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 PostgreSQL Setup for Quiz Application")
    print("=" * 50)
    
    # Check if running as postgres user
    import os
    if os.getenv('USER') != 'postgres':
        print("⚠️  Warning: You may need to run this script as the postgres user.")
        print("   If you encounter permission errors, try:")
        print("   sudo -u postgres python setup_postgres.py")
        print()
    
    setup_database() 