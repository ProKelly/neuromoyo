"""Thin wrapper around Supabase Auth's Admin API -- just enough to invite a new
clinician by email. No supabase-py dependency; this is one HTTP call, and a
direct call keeps the dependency footprint (and what's happening) obvious.

Requires SUPABASE_SERVICE_ROLE_KEY, which must NEVER reach the frontend -- it
grants full admin access to the Supabase project, not just this app's data.
"""
from __future__ import annotations

import httpx
from fastapi import HTTPException

from .config import get_settings

settings = get_settings()


async def invite_user_by_email(email: str) -> dict:
    """Creates an unconfirmed Supabase Auth user and sends them an invite email
    (set-password link). Returns the created user object, notably its `id` --
    which becomes the new Clinician row's primary key immediately, so there's no
    "auto-provisioned but unscoped" gap for anyone who arrives through this flow
    (see routers/clinicians.py's `invite_clinician`).

    Passes `redirect_to` so the emailed link lands on the frontend's own
    set-password page (frontend/pages/accept-invite.vue) instead of Supabase's
    bare default -- without this, the link logs the person in with a temporary
    session and drops them on the app with no way to actually set a password,
    which is a dead end, not a login. That URL must ALSO be added in Supabase:
    Authentication -> URL Configuration -> Redirect URLs -- Supabase silently
    ignores any redirect_to that isn't on that allow-list and falls back to its
    default, which reproduces the exact same dead end.
    """
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must both be set on the backend "
                   "to send invites (Project Settings -> API -> service_role key -- keep this "
                   "secret, it's admin-level access to your whole Supabase project).",
        )
    url = f"{settings.supabase_url.rstrip('/')}/auth/v1/invite"
    headers = {
        "apikey": settings.supabase_service_role_key,
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
        "Content-Type": "application/json",
    }
    redirect_to = f"{settings.frontend_url.rstrip('/')}/accept-invite"
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(url, headers=headers, params={"redirect_to": redirect_to}, json={"email": email})
    if resp.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="Supabase's built-in email sender is rate-limited (a handful of emails per "
                   "hour on the default/free tier -- meant for testing, not real onboarding "
                   "volume). Configure a custom SMTP provider under Project Settings -> "
                   "Authentication -> SMTP Settings to lift this, then retry.",
        )
    if resp.status_code == 422 or (resp.status_code == 400 and "already" in resp.text.lower()):
        raise HTTPException(status_code=409, detail=f"{email} has already been invited or has an account.")
    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Supabase invite failed ({resp.status_code}): {resp.text[:300]}")
    return resp.json()
