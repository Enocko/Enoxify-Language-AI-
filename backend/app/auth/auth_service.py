from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from datetime import timedelta
from ..models.database_models import User
from ..models.user_models import UserCreate, UserLogin
from .auth_utils import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def _normalize_email(self, email: str) -> str:
        # Avoid login failures due to casing or stray whitespace.
        return (email or "").strip().lower()

    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        email = self._normalize_email(user.email)

        # Check if user already exists
        db_user = self.db.query(User).filter(func.lower(User.email) == email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=email,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, user: UserLogin) -> User:
        """Authenticate a user"""
        email = self._normalize_email(user.email)
        db_user = self.db.query(User).filter(func.lower(User.email) == email).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        return db_user

    def create_user_token(self, user: User) -> dict:
        """Create access token for user"""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_email": user.email
        } 