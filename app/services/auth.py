from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import security_helper

class AuthService:
    @staticmethod
    def register_new_user(db: Session, user_data: UserCreate):
        """Registers a user after checking for email uniqueness."""
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        new_user = User(
            email=user_data.email,
            hashed_password=security_helper.hash_password(user_data.password),
            salt="bcrypt_internal"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """Verifies credentials and returns user object if successful."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not security_helper.verify_password(password, user.hashed_password):
            return None
        return user

auth_service = AuthService()