"""Database engine/session, pointed at Supabase Postgres via DATABASE_URL.

For the MVP we use SQLModel's `create_all` (see `init_db`) instead of Alembic
migrations. That's fine while the schema is still moving fast; once Phase 1
(NeuroVoice) is stable, switch to Alembic so schema changes are reviewable and
reversible rather than "whatever create_all currently produces."

Engine creation is lazy (built on first use, not at import time): this lets the
app boot and serve non-DB routes (e.g. voice inference smoke tests, /api/health)
even if DATABASE_URL isn't set yet, instead of crashing on import.
"""
from __future__ import annotations

from functools import lru_cache

from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine

from .config import get_settings

settings = get_settings()


@lru_cache
def get_engine():
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy backend/.env.example to backend/.env "
            "and paste in your Supabase Postgres connection string."
        )
    # pool_pre_ping avoids stale-connection errors against Supabase's pooler, which
    # can recycle idle connections.
    return create_engine(settings.sqlalchemy_database_url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    """Create tables that don't exist yet. Safe to call on every startup."""
    from . import models  # noqa: F401  (ensures models are registered on SQLModel.metadata)
    SQLModel.metadata.create_all(get_engine())


def get_session():
    try:
        engine = get_engine()
    except RuntimeError as e:
        # Surface as a clean 500 instead of an unhandled exception per-request.
        raise HTTPException(status_code=500, detail=str(e))
    with Session(engine) as session:
        yield session
