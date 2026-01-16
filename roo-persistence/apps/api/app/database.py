"""
Database configuration and connection management.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./roo_code_data.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=os.getenv("DEBUG", "false").lower() == "true",
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    """
    try:
        # Import all models to ensure they are registered with Base
        from app import models  # noqa: F401

        Base.metadata.create_all(bind=engine)
        print("✅ Database and tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise


def reset_db() -> None:
    """
    Reset the database by dropping and recreating all tables.
    """
    try:
        # Import all models to ensure they are registered with Base
        from app import models  # noqa: F401

        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Database reset successfully!")
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        raise
