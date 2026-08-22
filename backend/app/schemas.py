from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class PatientCreate(BaseModel):
    display_id: str
    age: int | None = None
    sex: str | None = None
    language: str | None = None
    facility: str | None = None
    existing_pd_diagnosis: bool | None = None
    on_pd_medication: bool | None = None


class PatientRead(PatientCreate):
    id: uuid.UUID
    created_at: datetime


class BiomarkerRead(BaseModel):
    code: str
    label: str
    value: float
    shap_contribution: float | None = None


class AssessmentRead(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    modality: str
    task: str
    performer: str | None
    model_name: str | None
    model_version: str | None
    quality_score: float | None
    risk_score: float | None
    confidence: float | None
    risk_band: str | None
    flagged: bool | None
    narrative: str | None
    voiced_sec: float | None
    n_windows: int | None
    n_recordings: int | None
    created_at: datetime
    biomarkers: list[BiomarkerRead] = []


class ScreenResultOut(BaseModel):
    """What the API returns right after scoring -- assessment fields flattened,
    plus fields the old Cadence UI relied on (narrative, top_factors, disclaimer)."""
    ok: bool
    error: str | None = None
    assessment_id: uuid.UUID | None = None
    modality: str | None = None
    task: str | None = None
    risk_score: float | None = None
    threshold: float | None = None
    flagged: bool | None = None
    risk_band: str | None = None
    confidence: float | None = None
    quality_score: float | None = None
    voiced_sec: float | None = None
    n_windows: int | None = None
    n_recordings: int | None = None
    narrative: str | None = None
    biomarkers: list[BiomarkerRead] = []
    disclaimer: str | None = None
