from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

def _get_database_url() -> str:
    """
    Prefer DATABASE_URL if set (Postgres etc).
    Otherwise use a writable SQLite path (safe for Docker/Render).
    """
    env_url = (os.getenv("DATABASE_URL") or "").strip()
    if env_url:
        # SQLAlchemy expects "postgresql://" (Render/Railway often provide "postgres://").
        if env_url.startswith("postgres://"):
            return "postgresql://" + env_url[len("postgres://") :]
        return env_url

    sqlite_path = (os.getenv("SQLITE_DB_PATH") or "").strip()
    if not sqlite_path:
        # /tmp is writable in most container platforms.
        sqlite_path = "/tmp/enoxify/users.db"

    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    return f"sqlite:///{sqlite_path}"


SQLALCHEMY_DATABASE_URL = _get_database_url()

# Create engine
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    connect_args = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

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