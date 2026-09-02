from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_clinician, require_admin, require_facility_admin
from ..db import get_session
from ..models import Clinician, Facility
from ..schemas import ClinicianRead, ClinicianUpdate, InviteClinicianPayload
from ..supabase_admin import invite_user_by_email

router = APIRouter(prefix="/api/clinicians", tags=["clinicians"])


@router.get("/me", response_model=ClinicianRead)
def read_current_clinician(clinician: Clinician = Depends(get_current_clinician)):
    """Lets the console show 'who am I / what facility am I scoped to' after login."""
    return clinician


@router.get("", response_model=list[ClinicianRead])
def list_clinicians(
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(require_facility_admin),
):
    """Global admin sees every clinician; a facility_admin sees only their own
    facility's roster -- enough to manage their own team, nothing more."""
    stmt = select(Clinician)
    if clinician.role != "admin":
        stmt = stmt.where(Clinician.facility_id == clinician.facility_id)
    return session.exec(stmt).all()


@router.post("/invite", response_model=ClinicianRead)
async def invite_clinician(
    payload: InviteClinicianPayload,
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(require_facility_admin),
):
    """Sends a Supabase invite email and creates the Clinician row immediately
    with the right role/facility already set -- so accepting the invite is the
    ONLY step left; there's no "logs in, sees nothing, needs manual promotion"
    gap for anyone who arrives through this flow (contrast with app/auth.py's
    auto-provision fallback, which still exists only for the bootstrap admin).

    Permission rules:
    - A facility_admin can only invite a "clinician" (never another
      facility_admin or an admin) to their OWN facility.
    - A global admin can invite either role, to any facility.
    - Global "admin" itself is never invitable through this endpoint -- that
      role is promoted by hand-editing the database, a deliberate extra step
      for the most powerful role (see Clinician's docstring in models.py).
    """
    if payload.role not in ("clinician", "facility_admin"):
        raise HTTPException(status_code=400, detail="role must be 'clinician' or 'facility_admin'.")

    if clinician.role == "facility_admin":
        if payload.role != "clinician":
            raise HTTPException(status_code=403, detail="A facility admin can only invite clinicians, not other admins.")
        if payload.facility_id != clinician.facility_id:
            raise HTTPException(status_code=403, detail="You can only invite clinicians to your own facility.")

    facility = session.get(Facility, payload.facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found.")

    existing = session.exec(select(Clinician).where(Clinician.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"{payload.email} is already a registered clinician.")

    supabase_user = await invite_user_by_email(payload.email)
    new_clinician = Clinician(
        id=uuid.UUID(supabase_user["id"]), email=payload.email,
        role=payload.role, facility_id=facility.id, facility=facility.name,
    )
    session.add(new_clinician)
    session.commit()
    session.refresh(new_clinician)
    return new_clinician


@router.patch("/{clinician_id}", response_model=ClinicianRead)
def update_clinician(
    clinician_id: uuid.UUID,
    payload: ClinicianUpdate,
    session: Session = Depends(get_session),
    _admin: Clinician = Depends(require_admin),
):
    """Global-admin only -- assign facility / promote role directly. This is how
    the very first bootstrap login (auto-provisioned with role="clinician",
    facility=None, and therefore able to see zero patients) gets scoped, before
    any invite system has been used yet. Once facilities exist, prefer
    POST /api/clinicians/invite for onboarding new people -- it sets role and
    facility correctly from the start instead of needing this as a follow-up."""
    clinician = session.get(Clinician, clinician_id)
    if not clinician:
        raise HTTPException(status_code=404, detail="Clinician not found")
    data = payload.model_dump(exclude_unset=True)
    if "role" in data and data["role"] not in ("clinician", "facility_admin", "admin"):
        raise HTTPException(status_code=400, detail="role must be 'clinician', 'facility_admin', or 'admin'")
    for field, value in data.items():
        setattr(clinician, field, value)
    session.add(clinician)
    session.commit()
    session.refresh(clinician)
    return clinician
