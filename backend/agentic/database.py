"""
Database layer for CoreAI.

Uses PostgreSQL in production (set DATABASE_URL, e.g.
postgresql://user:pass@localhost:5432/coreai) and falls back to a local
SQLite file for zero-config development/tests.
"""
import os
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///coreai.db")

# SQLite needs this connect_arg for multi-threaded Flask dev server use.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True)
    thread_id = Column(String(128), index=True, nullable=False)
    role = Column(String(16), nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    agent = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    thread_id = Column(String(128), index=True, nullable=False)
    title = Column(String(256), nullable=False)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class MemoryItem(Base):
    __tablename__ = "memory_items"

    id = Column(Integer, primary_key=True)
    key = Column(String(128), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create tables if they don't exist. Safe to call on every startup."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    """Context-managed DB session: `with get_session() as db: ...`"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
