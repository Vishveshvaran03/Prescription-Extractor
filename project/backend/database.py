"""
Database connection module for Supabase PostgreSQL.
Uses SQLAlchemy ORM with psycopg2-binary driver.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file (in project root, one level up)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set!\n"
        "Please configure your Supabase credentials in the .env file.\n"
        "See supabase_setup.md for instructions."
    )

# Create SQLAlchemy engine
# pool_pre_ping=True ensures stale connections are recycled (important for cloud DBs)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern SQLAlchemy 2.x Base class
class Base(DeclarativeBase):
    pass

# Dependency to get DB session (used by FastAPI Depends)
def get_db():
    """Yields a database session and ensures it's closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
