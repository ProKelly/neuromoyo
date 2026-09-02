from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_clinician
from ..db import get_session
from ..models import Assessment, Clinician, Patient
from ..reporting import build_report
from ..schemas import AssessmentRead, BiomarkerRead, PatientCreate, PatientRead, PatientReport, PatientUpdate

router = APIRouter(prefix="/api/patients", tags=["patients"])


def _assert_can_access(patient: Patient, clinician: Clinician) -> None:
    """Admins see every patient. A clinician only sees patients at their own
    assigned facility -- and a clinician with no facility assigned yet (the
    auto-provisioned default on first login) can see none, by design, until an
    admin scopes them (see PATCH /api/clinicians/{id})."""
    if clinician.role == "admin":
        return
    if not clinician.facility or patient.facility != clinician.facility:
        raise HTTPException(status_code=404, detail="Patient not found")


@router.post("", response_model=PatientRead)
def create_patient(
    payload: PatientCreate,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    data = payload.model_dump()
    if clinician.role == "admin":
        # Admins aren't tied to one facility, so they must specify which one --
        # but see GET /api/facilities: the frontend offers this as a pick-list
        # of already-registered facilities rather than a free-typed field, so
        # the typo risk is minimized even here.
        if not data.get("facility"):
            raise HTTPException(status_code=422, detail="As an admin, you must specify which facility this patient belongs to.")
    else:
        # The common path: a clinician's own facility is the ONLY possible value,
        # so it's assigned server-side and never taken from client input at all --
        # this is what actually eliminates the typo risk, not just validating a
        # typed value against expectations after the fact.
        if not clinician.facility:
            raise HTTPException(
                status_code=403,
                detail="Your account isn't assigned to a facility yet. Ask an admin to set one "
                       "via PATCH /api/clinicians/{your_id} before you can register patients.",
            )
        data["facility"] = clinician.facility
    patient = Patient(**data)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.get("", response_model=list[PatientRead])
def list_patients(
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    stmt = select(Patient)
    if clinician.role != "admin":
        # No facility assigned yet -> see nothing, rather than every clinic's patients.
        stmt = stmt.where(Patient.facility == (clinician.facility or "__unassigned__"))
    return session.exec(stmt).all()


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: uuid.UUID,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    _assert_can_access(patient, clinician)
    return patient


@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: uuid.UUID,
    payload: PatientUpdate,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    """Edit a patient's own details. `facility` reassignment is admin-only --
    a clinician editing their own patient's facility string could otherwise be
    used to move a patient in or out of their own visibility, which is exactly
    the kind of scope violation _assert_can_access exists to prevent elsewhere."""
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    _assert_can_access(patient, clinician)

    updates = payload.model_dump(exclude_unset=True)
    if "facility" in updates and clinician.role != "admin":
        raise HTTPException(status_code=403, detail="Only an admin can reassign a patient to a different facility.")

    for field, value in updates.items():
        setattr(patient, field, value)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.get("/{patient_id}/assessments", response_model=list[AssessmentRead])
def list_patient_assessments(
    patient_id: uuid.UUID,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    """Longitudinal history for this patient -- the basis for NeuroMonitor trend
    views. Built explicitly (not returned via response_model auto-mapping) because
    `Assessment.observations` (the DB relationship name) and `AssessmentRead.biomarkers`
    (the API field name) don't share a name, so implicit ORM attribute matching
    would silently serialize every assessment with an empty biomarkers list."""
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    _assert_can_access(patient, clinician)

    stmt = select(Assessment).where(Assessment.patient_id == patient_id).order_by(Assessment.created_at)
    assessments = session.exec(stmt).all()
    return [
        AssessmentRead(
            id=a.id, patient_id=a.patient_id, modality=a.modality, task=a.task,
            performer=a.performer, model_name=a.model_name, model_version=a.model_version,
            quality_score=a.quality_score, risk_score=a.risk_score, confidence=a.confidence,
            risk_band=a.risk_band, flagged=a.flagged, narrative=a.narrative,
            voiced_sec=a.voiced_sec, n_windows=a.n_windows, n_recordings=a.n_recordings,
            created_at=a.created_at,
            biomarkers=[
                BiomarkerRead(code=o.code, label=o.label, value=o.value, shap_contribution=o.shap_contribution)
                for o in a.observations
            ],
        )
        for a in assessments
    ]


@router.get("/{patient_id}/report", response_model=PatientReport)
def get_patient_report(
    patient_id: uuid.UUID,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    """Cross-task synthesized report -- see app/reporting.py for how the
    recommendation is derived. Built fresh on every request (cheap at this
    data volume); worth caching only if a facility's assessment history grows
    large enough to make the trend computation noticeably slow."""
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    _assert_can_access(patient, clinician)

    stmt = select(Assessment).where(Assessment.patient_id == patient_id).order_by(Assessment.created_at)
    assessments = session.exec(stmt).all()
    for a in assessments:
        _ = a.observations  # touch the relationship while the session is open (lazy-loaded)
    return build_report(patient, list(assessments))
