"""Security utilities for authentication"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer scheme for token extraction
# auto_error=False allows us to handle errors manually
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Ensure SECRET_KEY is a string
    secret_key = str(settings.SECRET_KEY)
    if len(secret_key) < 32:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"SECRET_KEY is too short ({len(secret_key)} chars). Should be at least 32 characters.")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    # Ensure we return a string (python-jose may return bytes in some versions)
    if isinstance(encoded_jwt, bytes):
        return encoded_jwt.decode('utf-8')
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        # Ensure SECRET_KEY is a string and token is a string
        secret_key = str(settings.SECRET_KEY)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"JWT decode error: {str(e)}. Token: {token[:50] if isinstance(token, str) else 'bytes'}... Secret key length: {len(secret_key)}")
        return None
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error decoding token: {str(e)}. Type: {type(e).__name__}")
        return None


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = None
    
    # First, try to get token from Authorization header directly (most reliable)
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif credentials is not None:
        # Fallback: Try to get token from HTTPBearer
        token = credentials.credentials
    
    # If still no token, raise exception with debug info
    if not token:
        import logging
        logger = logging.getLogger(__name__)
        all_headers = {k: v for k, v in request.headers.items()}
        logger.warning(f"No token found. Headers: {all_headers}")
        raise credentials_exception
    
    # Decode and validate token
    payload = decode_access_token(token)
    if payload is None:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Token decode failed. Token: {token[:20]}...")
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    # Convert user_id from string to int (JWT sub must be string)
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


