from uuid import UUID
from fastapi import HTTPException, Depends, status, Cookie
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings 

def get_current_user(
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(None) 
) -> User:
    """
    Dependency that validates the JWT from cookies and returns the current user.
    Uses settings for security parameters as required by Lab #4 architecture.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated: No session cookie found"
        )

    try:
 
        token_data = access_token.split(" ")[1] if " " in access_token else access_token
        
        payload = jwt.decode(
            token_data, 
            settings.JWT_ACCESS_SECRET, 
            algorithms=[settings.ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: Subject (sub) missing")
            
        current_user_uuid = UUID(user_id)
        
    except (JWTError, IndexError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials: Token is malformed or expired"
        )

    user = db.query(User).filter(User.id == current_user_uuid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found in the system")
    
    return user