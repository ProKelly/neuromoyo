from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_clinician, require_admin
from ..db import get_session
from ..models import Clinician
from ..schemas import ClinicianRead, ClinicianUpdate

router = APIRouter(prefix="/api/clinicians", tags=["clinicians"])


@router.get("/me", response_model=ClinicianRead)
def read_current_clinician(clinician: Clinician = Depends(get_current_clinician)):
    """Lets the console show 'who am I / what facility am I scoped to' after login."""
    return clinician


@router.get("", response_model=list[ClinicianRead])
def list_clinicians(
    session: Session = Depends(get_session),
    _admin: Clinician = Depends(require_admin),
):
    """Admin-only -- lets an admin see who has logged in and assign them a facility/role."""
    return session.exec(select(Clinician)).all()


@router.patch("/{clinician_id}", response_model=ClinicianRead)
def update_clinician(
    clinician_id: uuid.UUID,
    payload: ClinicianUpdate,
    session: Session = Depends(get_session),
    _admin: Clinician = Depends(require_admin),
):
    """Admin-only -- assign facility / promote role. This is how a brand-new login
    (auto-provisioned with role="clinician", facility=None, and therefore able to
    see zero patients) gets scoped to real data."""
    clinician = session.get(Clinician, clinician_id)
    if not clinician:
        raise HTTPException(status_code=404, detail="Clinician not found")
    data = payload.model_dump(exclude_unset=True)
    if "role" in data and data["role"] not in ("clinician", "admin"):
        raise HTTPException(status_code=400, detail="role must be 'clinician' or 'admin'")
    for field, value in data.items():
        setattr(clinician, field, value)
    session.add(clinician)
    session.commit()
    session.refresh(clinician)
    return clinician
