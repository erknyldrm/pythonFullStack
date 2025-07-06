#!/usr/bin/env python3
"""
Database migration script to add new fields for enhanced admin registration
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import settings
import re

def get_connection():
    """Get database connection"""
    # Extract connection details from DATABASE_URL
    # Format: postgresql://username:password@host:port/database
    url = settings.database_url
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', url)
    
    if not match:
        raise ValueError("Invalid DATABASE_URL format")
    
    username, password, host, port, database = match.groups()
    
    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=username,
        password=password
    )

def migrate_database():
    """Run database migrations"""
    print("🔄 Starting database migration...")
    
    try:
        conn = get_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if new columns exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'admin_users' 
            AND column_name IN ('first_name', 'last_name', 'role', 'is_email_verified', 'email_verification_token', 'password_reset_token', 'password_reset_expires', 'last_login')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns
        migrations = [
            ("first_name", "ALTER TABLE admin_users ADD COLUMN first_name VARCHAR(50)"),
            ("last_name", "ALTER TABLE admin_users ADD COLUMN last_name VARCHAR(50)"),
            ("role", "ALTER TABLE admin_users ADD COLUMN role VARCHAR(20) DEFAULT 'admin'"),
            ("is_email_verified", "ALTER TABLE admin_users ADD COLUMN is_email_verified BOOLEAN DEFAULT FALSE"),
            ("email_verification_token", "ALTER TABLE admin_users ADD COLUMN email_verification_token VARCHAR(255)"),
            ("password_reset_token", "ALTER TABLE admin_users ADD COLUMN password_reset_token VARCHAR(255)"),
            ("password_reset_expires", "ALTER TABLE admin_users ADD COLUMN password_reset_expires TIMESTAMP WITH TIME ZONE"),
            ("last_login", "ALTER TABLE admin_users ADD COLUMN last_login TIMESTAMP WITH TIME ZONE")
        ]
        
        for column_name, sql in migrations:
            if column_name not in existing_columns:
                try:
                    cursor.execute(sql)
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    print(f"⚠️  Column {column_name} already exists or error: {e}")
            else:
                print(f"⏭️  Column {column_name} already exists")
        
        # Check if admin_invitations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'admin_invitations'
            )
        """)
        
        result = cursor.fetchone()
        invitations_table_exists = result[0] if result else False
        
        if not invitations_table_exists:
            print("📧 Creating admin_invitations table...")
            cursor.execute("""
                CREATE TABLE admin_invitations (
                    id SERIAL PRIMARY KEY,
                    invitation_id VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    role VARCHAR(20) DEFAULT 'admin',
                    invited_by INTEGER REFERENCES admin_users(id),
                    is_used BOOLEAN DEFAULT FALSE,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Created admin_invitations table")
        else:
            print("⏭️  admin_invitations table already exists")
        
        # Update existing admin user to have proper role
        cursor.execute("""
            UPDATE admin_users 
            SET role = 'super_admin', is_email_verified = TRUE 
            WHERE username = 'admin'
        """)
        
        if cursor.rowcount > 0:
            print("✅ Updated default admin user")
        
        conn.close()
        print("🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate_database() 