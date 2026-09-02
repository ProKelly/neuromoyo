from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_clinician, require_admin
from ..db import get_session
from ..models import Clinician, Facility
from ..schemas import FacilityCreate, FacilityRead

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@router.get("", response_model=list[FacilityRead])
def list_facilities(
    session: Session = Depends(get_session),
    _clinician: Clinician = Depends(get_current_clinician),
):
    """Any authenticated clinician can list facilities -- needed for the admin
    intake-form picker and the invite flow. This is metadata (facility names),
    not patient data, so it's fine for a plain clinician to see the full list
    even though they can't act on facilities they don't belong to."""
    return session.exec(select(Facility).order_by(Facility.name)).all()


@router.post("", response_model=FacilityRead)
def create_facility(
    payload: FacilityCreate,
    session: Session = Depends(get_session),
    admin: Clinician = Depends(require_admin),
):
    """Global-admin only, deliberately -- see Facility's docstring in models.py
    for why facility creation is gated rather than self-serve."""
    existing = session.exec(select(Facility).where(Facility.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"A facility named '{payload.name}' already exists.")
    facility = Facility(name=payload.name, created_by=admin.id)
    session.add(facility)
    session.commit()
    session.refresh(facility)
    return facility
