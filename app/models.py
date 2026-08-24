"""Core data model.

Deliberately generic across modalities (per the engineering blueprint, §2/§4.1):
there is exactly ONE `Assessment` table and ONE `Observation` table, never
`voice_assessments` / `gait_assessments`. A row's `modality` field ("voice" today,
"tapping"/"gait"/... later) is what distinguishes it -- so adding a modality is new
rows, not a schema migration.

Field names loosely mirror FHIR (`Patient`, `Observation`, `DiagnosticReport`-ish
`Assessment`) so a future FHIR export/import adapter is a thin translation layer,
not a rewrite.
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Clinician(SQLModel, table=True):
    """A logged-in user of the console -- role/facility scoping lives here, not in
    the Supabase Auth token itself (the token only proves *who*, not *what they can
    see*). `id` deliberately matches the Supabase `auth.users.id` UUID rather than
    being auto-generated, so a verified token maps straight to a row with no extra
    lookup table.

    Row is auto-created on first successful login (see app/auth.py) with
    role="clinician" and no facility -- an admin assigns facility/role afterward via
    `PATCH /api/clinicians/{id}`. A clinician with no facility sees no patients
    (safe default) until assigned; this is deliberately restrictive for a first
    pilot rather than defaulting new logins to "see everything".
    """
    id: uuid.UUID = Field(primary_key=True)
    email: str = Field(index=True)
    full_name: str | None = None
    role: str = Field(default="clinician")  # "clinician" | "admin"
    facility: str | None = None  # must match Patient.facility text for scoping to apply
    created_at: datetime = Field(default_factory=_now)


class Patient(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    display_id: str = Field(index=True)  # clinic-assigned patient code, not a govt ID
    age: int | None = None
    sex: str | None = None
    language: str | None = None  # "en" | "fr" | ... -- drives voice task language
    facility: str | None = None  # clinic/site name, free text for MVP
    existing_pd_diagnosis: bool | None = None
    on_pd_medication: bool | None = None
    created_at: datetime = Field(default_factory=_now)

    assessments: List["Assessment"] = Relationship(back_populates="patient")


class Assessment(SQLModel, table=True):
    """One completed modality run (e.g. one voice screening pass).

    Top-level fields mirror the standardized `AssessmentModality` output shape from
    the blueprint (modality, model_name/version, quality_score, risk_score,
    confidence) so the API response and the DB row stay in lockstep.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    patient_id: uuid.UUID = Field(foreign_key="patient.id", index=True)

    modality: str = Field(index=True)  # "voice" (only implemented modality for now)
    task: str  # "reading" | "vowel" | "ddk"
    performer: str | None = None  # health worker identifier/name, free text for MVP

    model_name: str | None = None      # e.g. "voice_pd_v1"
    model_version: str | None = None   # e.g. "1.0.0"

    quality_score: float | None = None   # audio/signal quality gate, 0-1
    risk_score: float | None = None      # P(PD)-like probability, 0-1
    confidence: float | None = None      # window-agreement confidence, 0-1
    risk_band: str | None = None         # "low" | "moderate" | "elevated"
    flagged: bool | None = None

    narrative: str | None = None  # plain-language explanation shown to clinician
    voiced_sec: float | None = None
    n_windows: int | None = None
    n_recordings: int | None = None

    created_at: datetime = Field(default_factory=_now)

    patient: Patient = Relationship(back_populates="assessments")
    observations: List["Observation"] = Relationship(back_populates="assessment")


class Observation(SQLModel, table=True):
    """One biomarker measurement belonging to an Assessment.

    `code` is the raw feature key (e.g. `jitterLocal_sma3nz_amean`); `label` is the
    clinician-facing name. Never collapse this into a JSON blob on Assessment --
    keeping it row-per-biomarker is what lets a future FHIR export map each row to
    its own `Observation` resource, and what lets NeuroMonitor query trends per
    biomarker across time.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    assessment_id: uuid.UUID = Field(foreign_key="assessment.id", index=True)
    code: str
    label: str
    value: float
    shap_contribution: float | None = None  # signed contribution to risk_score, if available

    assessment: Assessment = Relationship(back_populates="observations")
