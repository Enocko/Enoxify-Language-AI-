from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user_models import UserCreate, UserLogin, Token, User
from .auth_service import AuthService
from .dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    auth_service = AuthService(db)
    return auth_service.create_user(user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and get access token"""
    auth_service = AuthService(db)
    db_user = auth_service.authenticate_user(user)
    return auth_service.create_user_token(db_user)

@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user 