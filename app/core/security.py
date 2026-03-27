from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes password with an automatic unique salt using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Checks if the plain password matches the stored hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Generates a signed JWT token for user sessions.
        Uses settings from config.py for secret key, algorithm, and expiry.
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_ACCESS_SECRET, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

security_helper = SecurityHelper()