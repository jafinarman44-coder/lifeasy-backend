"""
LIFEASY V30 PRO - Production Database Configuration
Supports both SQLite (dev) and PostgreSQL (production)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Environment-based configuration
ENV = os.getenv("LIFEASY_ENV", "development")

if ENV == "production":
    # PostgreSQL for production
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://lifeasy_user:123456@localhost/lifeasy"
    )
else:
    # SQLite for development
    DATABASE_URL = "sqlite:///./lifeasy_v30.db"

# Create engine
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,  # Enable connection health checks
        echo=False
    )
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized ({ENV} mode)")


if __name__ == "__main__":
    init_db()
