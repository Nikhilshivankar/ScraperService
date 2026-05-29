from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from app.core.config import get_config

config = get_config()

DATABASE_URL = config.DATABASE_URL

# Configure engine based on database type
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Use scoped_session for thread-safety
SessionLocal = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
