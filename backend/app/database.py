from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database URL.
# Use an absolute path so the DB doesn't change depending on where the backend is started from.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/app
_BACKEND_DIR = os.path.dirname(_THIS_DIR)  # backend
_DB_PATH = os.path.join(_BACKEND_DIR, "users.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{_DB_PATH}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 