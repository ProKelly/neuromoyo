"""Supabase Auth verification and clinician profile/role scoping.

The frontend authenticates directly against Supabase Auth (email + password --
see the console's /login page) and sends the resulting access token as
`Authorization: Bearer <token>` on every API call. This module:

1. Verifies that token. Supabase projects sign access tokens one of two ways
   depending on when the project was created / what's enabled:
     - Newer projects default to asymmetric signing keys (ES256/RS256) and
       publish the public key via a JWKS endpoint -- no shared secret needed,
       verified here with `PyJWKClient` (cached, refetched only on a `kid` miss).
     - Older projects (or ones with "Legacy JWT Secret" enabled) sign with a
       single HS256 shared secret (`SUPABASE_JWT_SECRET`).
   We try JWKS first (covers the current default and requires zero secret
   configuration beyond SUPABASE_URL), and fall back to the HS256 secret only
   for a token whose header actually says `alg: HS256`. Trying to verify an
   ES256 token against an HS256 secret (or vice versa) always fails outright
   with "the specified alg value is not allowed" -- that's a signing-method
   mismatch, not an expired/invalid session, so we don't conflate the two in
   the error message below.
2. Loads (or, on first login, creates) the matching `Clinician` profile row.
   Role and facility live in OUR database, not in the token, so revoking a
   clinician's access to a facility doesn't require touching Supabase Auth at
   all -- just editing their `Clinician` row.

Nothing here creates Supabase Auth *users* -- account creation happens in the
Supabase dashboard (Authentication -> Users -> Add user) or via Supabase's own
signup APIs. This module only ever reads a token that Supabase already issued.
"""
from __future__ import annotations

import uuid
from functools import lru_cache
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException
from sqlmodel import Session

from .config import get_settings
from .db import get_session
from .models import Clinician

settings = get_settings()

# Algorithms a Supabase-issued token might use, depending on project vintage/config.
_ASYMMETRIC_ALGS = ["ES256", "RS256"]


@lru_cache
def _jwks_client() -> "jwt.PyJWKClient | None":
    if not settings.supabase_url:
        return None
    jwks_url = f"{settings.supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    # cache_keys=True: keys are cached in-process and only refetched on a `kid` miss,
    # so this is not a network round-trip on every request.
    return jwt.PyJWKClient(jwks_url, cache_keys=True)


def _decode_token(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Malformed token: {e}")
    alg = header.get("alg")

    if alg in _ASYMMETRIC_ALGS:
        client = _jwks_client()
        if client is None:
            raise HTTPException(
                status_code=500,
                detail="SUPABASE_URL is not configured on the backend, so the JWKS "
                       "endpoint used to verify this project's tokens can't be reached "
                       "(see backend/.env.example).",
            )
        try:
            signing_key = client.get_signing_key_from_jwt(token)
            return jwt.decode(token, signing_key.key, algorithms=_ASYMMETRIC_ALGS, audience="authenticated")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired session: {e}")

    if alg == "HS256":
        if not settings.supabase_jwt_secret:
            raise HTTPException(
                status_code=500,
                detail="This project signs tokens with HS256 but SUPABASE_JWT_SECRET is not "
                       "configured on the backend (Project Settings -> API -> JWT Settings -> "
                       "\"Legacy JWT Secret\" -- see backend/.env.example).",
            )
        try:
            return jwt.decode(token, settings.supabase_jwt_secret, algorithms=["HS256"], audience="authenticated")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired session: {e}")

    raise HTTPException(status_code=401, detail=f"Unsupported token signing algorithm: {alg!r}")


def get_current_clinician(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session),
) -> Clinician:
    """FastAPI dependency: verifies the bearer token and returns the caller's
    Clinician profile, auto-provisioning one on first successful login."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token. Log in and retry.")
    token = authorization.split(" ", 1)[1].strip()
    claims = _decode_token(token)

    try:
        user_id = uuid.UUID(str(claims["sub"]))
    except (KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token is missing a valid subject claim.")
    email = claims.get("email") or (claims.get("user_metadata") or {}).get("email") or ""

    clinician = session.get(Clinician, user_id)
    if clinician is None:
        clinician = Clinician(id=user_id, email=email, role="clinician")
        session.add(clinician)
        session.commit()
        session.refresh(clinician)
    elif email and clinician.email != email:
        # Email changed on the Supabase side (e.g. after a change-email flow) -- keep in sync.
        clinician.email = email
        session.add(clinician)
        session.commit()
        session.refresh(clinician)
    return clinician


def require_admin(clinician: Clinician = Depends(get_current_clinician)) -> Clinician:
    """Stricter dependency for admin-only routes (e.g. assigning facilities/roles)."""
    if clinician.role != "admin":
        raise HTTPException(status_code=403, detail="This action requires an admin role.")
    return clinician
