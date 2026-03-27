from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.auth import auth_service
from app.core.security import security_helper

router = APIRouter(tags=["Authentication"])

@router.post(
    "/register", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
    description="Registers a new user in the system. Hashes the password and saves the user record to the database.",
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "Bad Request: Email already registered or invalid data"},
        422: {"description": "Validation Error: Check input fields requirements"}
    }
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new account in the database.
    Password must be at least 8 characters long and contain at least one digit.
    """
    return auth_service.register_new_user(db, user_data)

@router.post(
    "/login",
    summary="User authentication and login",
    description=(
        "Authenticates the user using email and password. If successful, "
        "sets an **HttpOnly cookie** containing the JWT access token."
    ),
    responses={
        200: {
            "description": "Login successful. Cookie 'access_token' has been set.",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message": "User logged in"}
                }
            }
        },
        401: {"description": "Unauthorized: Invalid email or password"},
        422: {"description": "Validation Error: Incorrect input format"}
    }
)
def login(
    response: Response, 
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Logs the user in and sets an HttpOnly cookie with JWT.
    This cookie is protected against XSS and CSRF attacks.
    """
    user = auth_service.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
 
    token = security_helper.create_access_token(data={"sub": str(user.id)})
    
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,  # Mandatory protection against XSS
        max_age=3600,   # Session duration: 1 hour
        samesite="lax", # Basic protection against CSRF
        secure=False    # In development (localhost) set to False; in production should be True
    )
    
    return {"status": "success", "message": "User logged in"}

@router.post(
    "/logout",
    summary="User logout",
    description="Logs out the current user by instructing the browser to delete the session cookie.",
    responses={
        200: {"description": "Logout successful. Session cookie cleared."}
    }
)
def logout(response: Response):
    """
    Logs the user out by deleting the 'access_token' session cookie.
    """
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}