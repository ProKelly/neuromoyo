"""App settings, loaded from environment / .env.

DATABASE_URL is the Supabase Postgres connection string (Session pooler or direct
connection, both work with SQLAlchemy). Get it from:
  Supabase dashboard -> Project Settings -> Database -> Connection string -> URI

It looks like:
  postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres

SQLAlchemy needs the psycopg driver prefix, so we normalize `postgresql://` to
`postgresql+psycopg://` in `sqlalchemy_database_url` below -- paste the Supabase
URI as-is into .env, no manual editing needed.
"""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent  # backend/
ARTIFACTS_DIR = ROOT / "artifacts"
CACHE_DIR = ROOT / ".cache"
for _d in (ARTIFACTS_DIR, CACHE_DIR):
    _d.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Supabase / Postgres ---
    database_url: str = ""  # required in real use; empty only breaks DB-backed routes
    supabase_url: str = ""
    supabase_service_role_key: str = ""  # server-side only, never expose to frontend
    supabase_jwt_secret: str = ""        # "Legacy JWT Secret" (HS256) -- verifies clinician session tokens

    # --- App ---
    environment: str = "development"
    cors_origins: str = "*"  # comma-separated list in prod, e.g. "https://app.neuromoyo.com"
    # Public URL of the FRONTEND (not this backend) -- used only to build the
    # redirect_to link in clinician invite emails (app/supabase_admin.py), so a
    # clicked invite lands on OUR set-password page instead of Supabase's bare
    # default. Must also be added to Supabase's Authentication -> URL
    # Configuration -> Redirect URLs allow-list, or Supabase silently ignores it.
    frontend_url: str = "http://localhost:3000"
    sample_rate: int = 16_000
    random_seed: int = 42

    @property
    def sqlalchemy_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
