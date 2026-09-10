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


class Facility(SQLModel, table=True):
    """A registered health facility -- gated creation only (see routers/facilities.py):
    a global admin creates the row and invites its first `facility_admin`, who then
    invites their own facility's clinicians. No self-serve signup, deliberately --
    this is a pre-validation clinical tool, not an open SaaS product yet (see the
    "What this actually does" framing in the README).

    `Patient.facility` / `Clinician.facility` stay as denormalized display-name
    strings (kept in sync with `Facility.name` at write time) rather than being
    switched to `facility_id` everywhere -- that keeps every existing scoping check
    and every frontend page that already reads `.facility` as a string working
    unchanged. `facility_id` on Clinician is the source of truth for onboarding
    (invites, the admin console); the string is what patient-scoping still compares.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=_now)
    created_by: uuid.UUID | None = Field(default=None, foreign_key="clinician.id")


class Clinician(SQLModel, table=True):
    """A logged-in user of the console -- role/facility scoping lives here, not in
    the Supabase Auth token itself (the token only proves *who*, not *what they can
    see*). `id` deliberately matches the Supabase `auth.users.id` UUID rather than
    being auto-generated, so a verified token maps straight to a row with no extra
    lookup table.

    Three-tier role: "admin" (global, sees/manages every facility, the only role
    that can register a new Facility -- promoted by hand-editing this table, never
    via the invite API, as a deliberate extra-friction safety measure for the most
    powerful role) > "facility_admin" (scoped to one facility, can invite/manage
    clinicians within it, patient-visibility otherwise identical to "clinician") >
    "clinician" (screening only).

    A row is normally created by `POST /api/clinicians/invite` at invite time, with
    role/facility already set -- see routers/clinicians.py. The auto-create-on-
    first-login fallback in app/auth.py (role="clinician", no facility, sees
    nothing until assigned) only fires for a Supabase user that was never invited
    through that flow, e.g. the very first bootstrap admin.
    """
    id: uuid.UUID = Field(primary_key=True)
    email: str = Field(index=True)
    full_name: str | None = None
    role: str = Field(default="clinician")  # "clinician" | "facility_admin" | "admin"
    facility_id: uuid.UUID | None = Field(default=None, foreign_key="facility.id")
    facility: str | None = None  # denormalized Facility.name; must match Patient.facility for scoping
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


class VoiceIntelligenceSession(SQLModel, table=True):
    """Auditable downstream voice-AI session. Raw audio is never stored.

    This table is intentionally separate from Assessment so the challenge layer
    can be removed without changing the existing Parkinson's assessment schema.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    patient_id: uuid.UUID = Field(foreign_key="patient.id", index=True)
    assessment_id: uuid.UUID | None = Field(default=None, foreign_key="assessment.id", index=True)
    language: str | None = None
    asr_provider: str
    asr_model: str
    transcript: str
    asr_latency_ms: float | None = None
    audio_duration_s: float | None = None
    audio_quality_score: float | None = None
    consent_confirmed: bool = False
    created_at: datetime = Field(default_factory=_now)

    findings: List["ClinicalFinding"] = Relationship(back_populates="session")


class ClinicalFinding(SQLModel, table=True):
    """One traceable clinical-information extraction from patient speech."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="voiceintelligencesession.id", index=True)
    category: str = Field(index=True)
    concept: str = Field(index=True)
    value: str | None = None
    status: str
    confidence: float
    evidence: str | None = None
    source: str = "patient_speech"

    session: VoiceIntelligenceSession = Relationship(back_populates="findings")
