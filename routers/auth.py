from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import and_
import secrets
import re
from typing import Optional
from database import get_db
from models import AdminUser, AdminInvitation
from schemas import (
    Token, AdminUserCreate, AdminUser as AdminUserSchema,
    AdminUserCreateEnhanced, AdminInvitation as AdminInvitationSchema,
    AdminInvitationResponse, PasswordResetRequest, PasswordReset,
    EmailVerification, AdminRegistrationResponse, AdminUserProfile
)
from auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user, verify_password
from config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


# Password validation function
def validate_password(password: str) -> dict:
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")
    
    return {"valid": len(errors) == 0, "errors": errors}


# Email validation function
def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Generate secure token
def generate_secure_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint for admin users"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=AdminRegistrationResponse)
async def register_admin_user(
    user: AdminUserCreateEnhanced,
    db: Session = Depends(get_db)
):
    """Enhanced admin user registration with validation"""
    
    # Validate password confirmation
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate password strength
    password_validation = validate_password(user.password)
    if not password_validation["valid"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Password validation failed: {'; '.join(password_validation['errors'])}"
        )
    
    # Validate email format
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate username format
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', user.username):
        raise HTTPException(
            status_code=400, 
            detail="Username must be 3-20 characters long and contain only letters, numbers, and underscores"
        )
    
    # Check if username already exists
    existing_user = db.query(AdminUser).filter(AdminUser.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(AdminUser).filter(AdminUser.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate role
    valid_roles = ["admin", "moderator", "super_admin"]
    if user.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}")
    
    hashed_password = get_password_hash(user.password)
    email_verification_token = generate_secure_token()
    
    db_user = AdminUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        email_verification_token=email_verification_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # TODO: Send email verification (implement email service)
    # send_verification_email(db_user.email, email_verification_token)
    
    return AdminRegistrationResponse(
        user=db_user,
        message="Admin user registered successfully. Please check your email for verification.",
        requires_email_verification=True
    )


@router.post("/register/invited", response_model=AdminRegistrationResponse)
async def register_with_invitation(
    invitation_id: str,
    user: AdminUserCreateEnhanced,
    db: Session = Depends(get_db)
):
    """Register admin user with invitation"""
    
    # Find and validate invitation
    invitation = db.query(AdminInvitation).filter(
        and_(
            AdminInvitation.invitation_id == invitation_id,
            AdminInvitation.is_used.is_(False),
            AdminInvitation.expires_at > datetime.utcnow()
        )
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=400, detail="Invalid or expired invitation")
    
    if invitation.email != user.email:
        raise HTTPException(status_code=400, detail="Email does not match invitation")
    
    # Validate password confirmation
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate password strength
    password_validation = validate_password(user.password)
    if not password_validation["valid"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Password validation failed: {'; '.join(password_validation['errors'])}"
        )
    
    # Check if username already exists
    existing_user = db.query(AdminUser).filter(AdminUser.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    
    db_user = AdminUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=invitation.role,
        is_email_verified=True  # Invited users are pre-verified
    )
    db.add(db_user)
    
    # Mark invitation as used
    invitation.is_used = True
    
    db.commit()
    db.refresh(db_user)
    
    return AdminRegistrationResponse(
        user=db_user,
        message="Admin user registered successfully with invitation.",
        requires_email_verification=False
    )


@router.post("/invite", response_model=AdminInvitationResponse)
async def invite_admin_user(
    invitation: AdminInvitationSchema,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    """Invite a new admin user (requires existing admin privileges)"""
    
    # Check if current user has permission to invite
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions to invite users")
    
    # Validate email format
    if not validate_email(invitation.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if email already exists
    existing_user = db.query(AdminUser).filter(AdminUser.email == invitation.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate role
    valid_roles = ["admin", "moderator"]
    if invitation.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}")
    
    # Generate invitation
    invitation_id = generate_secure_token()
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days expiry
    
    db_invitation = AdminInvitation(
        invitation_id=invitation_id,
        email=invitation.email,
        role=invitation.role,
        invited_by=current_user.id,
        expires_at=expires_at
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    
    # TODO: Send invitation email (implement email service)
    # send_invitation_email(invitation.email, invitation_id, current_user.username)
    
    return AdminInvitationResponse(
        invitation_id=invitation_id,
        email=invitation.email,
        role=invitation.role,
        expires_at=expires_at,
        invited_by=current_user.username
    )


@router.post("/password-reset-request")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    
    user = db.query(AdminUser).filter(AdminUser.email == request.email).first()
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Generate reset token
    reset_token = generate_secure_token()
    expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
    
    user.password_reset_token = reset_token
    user.password_reset_expires = expires_at
    db.commit()
    
    # TODO: Send password reset email (implement email service)
    # send_password_reset_email(user.email, reset_token)
    
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset")
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password with token"""
    
    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate password strength
    password_validation = validate_password(reset_data.new_password)
    if not password_validation["valid"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Password validation failed: {'; '.join(password_validation['errors'])}"
        )
    
    # Find user with valid reset token
    user = db.query(AdminUser).filter(
        and_(
            AdminUser.password_reset_token == reset_data.token,
            AdminUser.password_reset_expires > datetime.utcnow()
        )
    ).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    # Update password and clear reset token
    user.hashed_password = get_password_hash(reset_data.new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.post("/verify-email")
async def verify_email(
    verification: EmailVerification,
    db: Session = Depends(get_db)
):
    """Verify email address"""
    
    user = db.query(AdminUser).filter(
        AdminUser.email_verification_token == verification.token
    ).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user.is_email_verified = True
    user.email_verification_token = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.get("/me", response_model=AdminUserProfile)
async def read_users_me(current_user: AdminUser = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user


@router.get("/invitations", response_model=list[AdminInvitationResponse])
async def get_invitations(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_active_user)
):
    """Get all invitations (admin only)"""
    
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invitations = db.query(AdminInvitation).filter(
        AdminInvitation.is_used.is_(False),
        AdminInvitation.expires_at > datetime.utcnow()
    ).all()
    
    return [
        AdminInvitationResponse(
            invitation_id=inv.invitation_id,
            email=inv.email,
            role=inv.role,
            expires_at=inv.expires_at,
            invited_by=inv.inviter.username if inv.inviter else None
        )
        for inv in invitations
    ] 