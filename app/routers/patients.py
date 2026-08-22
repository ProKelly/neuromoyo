from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Patient, Assessment
from ..schemas import PatientCreate, PatientRead, AssessmentRead

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("", response_model=PatientRead)
def create_patient(payload: PatientCreate, session: Session = Depends(get_session)):
    patient = Patient(**payload.model_dump())
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.get("", response_model=list[PatientRead])
def list_patients(session: Session = Depends(get_session)):
    return session.exec(select(Patient)).all()


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: uuid.UUID, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/{patient_id}/assessments", response_model=list[AssessmentRead])
def list_patient_assessments(patient_id: uuid.UUID, session: Session = Depends(get_session)):
    """Longitudinal history for this patient -- the basis for NeuroMonitor trend views."""
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    stmt = select(Assessment).where(Assessment.patient_id == patient_id).order_by(Assessment.created_at)
    return session.exec(stmt).all()
