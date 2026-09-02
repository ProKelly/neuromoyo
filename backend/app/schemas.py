from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class ClinicianRead(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str | None
    role: str
    facility_id: uuid.UUID | None = None
    facility: str | None
    created_at: datetime


class ClinicianUpdate(BaseModel):
    """Admin-only: assign a clinician's facility and/or promote their role."""
    full_name: str | None = None
    role: str | None = None  # "clinician" | "facility_admin" | "admin"
    facility: str | None = None


class FacilityCreate(BaseModel):
    name: str


class FacilityRead(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime


class InviteClinicianPayload(BaseModel):
    email: str
    facility_id: uuid.UUID
    role: str = "clinician"  # "clinician" | "facility_admin" -- global "admin" is never invitable


class PatientCreate(BaseModel):
    display_id: str
    age: int | None = None
    sex: str | None = None
    language: str | None = None
    # Optional on input: a non-admin clinician never needs to send this -- the
    # server assigns it from their own Clinician.facility automatically (see
    # routers/patients.py). Only an admin's request can set it explicitly,
    # since admins aren't tied to one facility.
    facility: str | None = None
    existing_pd_diagnosis: bool | None = None
    on_pd_medication: bool | None = None


class PatientUpdate(BaseModel):
    """All fields optional -- send only what changed. `facility` is accepted here
    but routers/patients.py rejects it from a non-admin: reassigning a patient to
    a different facility is an admin action, not something a clinician should be
    able to do to their own record (it would be a way to move a patient out of
    -- or into -- your own visibility by editing a string)."""
    display_id: str | None = None
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


class TrendPoint(BaseModel):
    date: datetime
    value: float


class BiomarkerTrend(BaseModel):
    code: str
    label: str
    points: list[TrendPoint]
    direction: str  # "increasing" | "decreasing" | "stable" | "insufficient_data"


class TaskSummary(BaseModel):
    task: str  # "reading" | "vowel" | "ddk"
    count: int
    last_date: datetime | None
    latest_risk_score: float | None = None  # only ever set for "reading"
    latest_risk_band: str | None = None


class PatientReport(BaseModel):
    """A synthesized cross-task clinical summary -- the point being that no single
    task's output is the report; a neurologist reading this should see the same
    combined picture the AssessmentModality architecture was built to eventually
    fuse (see app/reporting.py), just assembled by rules today rather than a
    trained fusion model."""
    patient: PatientRead
    generated_at: datetime
    date_range_start: datetime | None
    date_range_end: datetime | None
    total_assessments: int
    task_summaries: list[TaskSummary]
    latest_reading: AssessmentRead | None
    reading_points: list[TrendPoint]
    reading_trend_direction: str | None  # "increasing" | "decreasing" | "stable" | "insufficient_data" | None
    biomarker_trends: list[BiomarkerTrend]
    recommendation_tier: str  # "priority_referral" | "monitor" | "routine" | "insufficient_data"
    recommendation_text: str
    supporting_findings: list[str]
    disclaimer: str
