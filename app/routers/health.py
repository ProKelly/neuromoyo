from __future__ import annotations

from fastapi import APIRouter

from ..config import get_settings

router = APIRouter(prefix="/api", tags=["health"])
settings = get_settings()


@router.get("/health")
def health():
    return {"ok": True, "service": "neuromoyo-backend"}


@router.get("/ready")
def ready():
    """Non-secret deployment readiness signal for platform health checks."""
    return {
        "ok": True,
        "service": "neuromoyo-backend",
        "voice_intelligence_enabled": settings.voice_intelligence_enabled,
        "sahara_configured": bool(settings.sahara_api_key),
        "database_configured": bool(settings.database_url),
    }
