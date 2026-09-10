from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ASRResult(BaseModel):
    provider: str
    model: str
    transcript: str
    language: str | None = None
    latency_ms: float
    audio_duration_s: float
    request_id: str | None = None


class ClinicalFindingOut(BaseModel):
    id: uuid.UUID | None = None
    category: str
    concept: str
    value: str | None = None
    status: str
    confidence: float = Field(ge=0, le=1)
    evidence: str | None = None
    source: str = "patient_speech"


class VoiceIntelligenceOut(BaseModel):
    ok: bool
    error: str | None = None
    session_id: uuid.UUID | None = None
    assessment_id: uuid.UUID | None = None
    transcript: str | None = None
    language: str | None = None
    asr_provider: str | None = None
    asr_model: str | None = None
    asr_latency_ms: float | None = None
    audio_duration_s: float | None = None
    audio_quality_score: float | None = None
    clinical_findings: list[ClinicalFindingOut] = []
    neurological_signal: dict | None = None
    clinician_summary: str | None = None
    safety_notes: list[str] = []
    created_at: datetime | None = None
