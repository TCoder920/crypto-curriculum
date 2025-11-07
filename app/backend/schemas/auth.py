"""Authentication schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.backend.models.user import UserRole


class UserRegister(BaseModel):
    """User registration schema
    
    Note: All registrations are automatically assigned STUDENT role.
    Admin and instructor roles can only be assigned via seed script or admin endpoint.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    # Role is always STUDENT for new registrations - removed from schema for security


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: Optional[str]
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str = Field(..., min_length=8, description="New password must be at least 8 characters")

