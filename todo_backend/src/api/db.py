from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger("todo_backend.db")

# Determine database URL. Prefer env var if provided; fallback to local SQLite file.
# Do not hardcode secrets. If changed, update .env.example accordingly.
DB_URL = os.getenv("DATABASE_URL") or "sqlite:///./todo.db"

# SQLite specific: needed for multithreaded FastAPI usage
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Create engine with basic validation/logging for easier diagnostics on startup.
try:
    engine: Engine = create_engine(DB_URL, connect_args=connect_args, future=True)
    logger.info("Database engine created successfully", extra={"db_url": DB_URL})
except Exception:
    # Provide a clear error message that helps identify misconfiguration.
    logger.exception("Failed to create database engine for DATABASE_URL=%s", DB_URL)
    raise

# Global session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_db() -> None:
    """
    Initialize the database: create the tasks table if it does not exist.
    Using raw SQL to avoid requiring SQLAlchemy ORM Base metadata for a single table.
    """
    logger.info("Initializing database schema (tasks table)...")
    try:
        with engine.begin() as conn:
            # Simple migration: ensure tasks table exists
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        completed INTEGER NOT NULL DEFAULT 0,
                        created_at TEXT NOT NULL DEFAULT (datetime('now')),
                        updated_at TEXT NOT NULL DEFAULT (datetime('now'))
                    )
                    """
                )
            )
        logger.info("Database schema initialization complete.")
    except Exception:
        logger.exception("Database initialization failed")
        raise


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.
    This is used as a dependency in FastAPI routes.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        logger.exception("Database session error; transaction rolled back.")
        raise
    finally:
        session.close()
