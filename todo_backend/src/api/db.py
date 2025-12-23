from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

# Determine database URL. Prefer env var if provided; fallback to local SQLite file.
# Do not hardcode secrets. If changed, update .env.example accordingly.
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# SQLite specific: needed for multithreaded FastAPI usage
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Global engine and session maker
engine: Engine = create_engine(DB_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_db() -> None:
    """
    Initialize the database: create the tasks table if it does not exist.
    Using raw SQL to avoid requiring SQLAlchemy ORM Base metadata for a single table.
    """
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
        # Trigger-like behavior for updated_at on update (SQLite does not support triggers without CREATE TRIGGER)
        # We'll handle updated_at in application code during updates.


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
        raise
    finally:
        session.close()
