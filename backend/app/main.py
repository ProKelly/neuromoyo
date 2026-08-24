"""Neuromoyo backend (FastAPI).

Single-service API for the clinical CRUD (patients/assessments) and voice-modality
inference. Persists to Supabase Postgres via DATABASE_URL (see .env.example).
Audio is never stored -- each upload is written to a temp file, analyzed, and
deleted; only derived biomarkers/scores are persisted (see routers/assessments.py).
"""
from __future__ import annotations

import gc
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .db import init_db
from .routers import health, patients, assessments, clinicians

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist yet (MVP; move to Alembic once schema stabilizes).
    if settings.database_url:
        init_db()
    else:
        print("WARNING: DATABASE_URL is not set -- patient/assessment routes will fail. "
              "Add your Supabase connection string to backend/.env")

    if not settings.supabase_jwt_secret and not settings.supabase_url:
        print("WARNING: Neither SUPABASE_URL nor SUPABASE_JWT_SECRET is set -- every "
              "authenticated route will return 401/500. Set SUPABASE_URL (covers the "
              "default ES256/JWKS signing most Supabase projects use) and/or "
              "SUPABASE_JWT_SECRET (only needed for older HS256 \"Legacy JWT Secret\" "
              "projects) in backend/.env, then RESTART this process -- editing .env alone "
              "does not take effect on a running --reload server, since settings are only "
              "read once at process startup.")

    # Warm the voice model + SHAP explainer once so the first request is fast.
    print("Starting warm-up: loading voice model and SHAP explainer...")
    try:
        from .modalities.voice.model import load_model
        from .modalities.voice.explain import _explainer
        bundle = load_model()
        _ = _explainer(bundle)
        gc.collect()
        print(f"Warm-up complete. Voice model ready with {len(bundle['feature_names'])} features.")
    except Exception as e:  # pragma: no cover
        print(f"Warm-up warning: {e}")
    yield


app = FastAPI(title="Neuromoyo API", description="AI-assisted neurological screening (voice modality)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(patients.router)
app.include_router(assessments.router)
app.include_router(clinicians.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Safety net: any exception that escapes a route (e.g. a DB write failure
    outside a route's own try/except) still gets logged with a full traceback
    and returned as JSON `{"detail": ...}` instead of a bare, bodyless 500 --
    so the frontend's error surfacing (see useApi.ts / assess page) actually
    has something to show, and the server log has something to grep for."""
    import traceback
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": f"{type(exc).__name__}: {exc}"})


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.environment == "development")
