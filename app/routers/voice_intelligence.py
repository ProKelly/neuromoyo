from __future__ import annotations

import logging
import os
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from ..auth import get_current_clinician
from ..config import get_settings
from ..db import get_session
from ..models import Assessment, ClinicalFinding, Clinician, Observation, Patient, VoiceIntelligenceSession
from ..schemas import VoiceIntelligenceOut, VoiceIntelligenceRead, ClinicalFindingRead
from ..voice_intelligence.service import analyse

settings = get_settings()
logger = logging.getLogger("neuromoyo.voice_intelligence")
router = APIRouter(prefix="/api/voice-intelligence", tags=["voice-intelligence"])


def _require_patient(session: Session, patient_id: uuid.UUID, clinician: Clinician) -> Patient:
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if clinician.role != "admin" and (not clinician.facility or patient.facility != clinician.facility):
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


async def _save_temp(upload: UploadFile) -> str:
    if not upload.filename:
        suffix = ".webm"
    else:
        suffix = Path(upload.filename).suffix.lower() or ".webm"
    allowed = {".webm", ".wav", ".ogg", ".mp3", ".m4a", ".mp4", ".flac"}
    if suffix not in allowed:
        raise HTTPException(status_code=415, detail="Unsupported audio format.")
    allowed_mimes = {
        "audio/webm", "audio/wav", "audio/x-wav", "audio/ogg",
        "audio/mpeg", "audio/mp4", "audio/x-m4a", "audio/flac",
        "application/octet-stream",
    }
    if upload.content_type and upload.content_type.lower() not in allowed_mimes:
        raise HTTPException(status_code=415, detail="Unsupported audio media type.")

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        path = tmp.name
        total = 0
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > 25 * 1024 * 1024:
                os.unlink(path)
                raise HTTPException(status_code=413, detail="Audio upload is too large.")
            tmp.write(chunk)
    if total == 0:
        os.unlink(path)
        raise HTTPException(status_code=400, detail="Empty audio upload.")
    return path


@router.post("/analyse", response_model=VoiceIntelligenceOut)
async def analyse_voice(
    patient_id: uuid.UUID = Form(...),
    language: str = Form("en"),
    consent_confirmed: bool = Form(False),
    audio: UploadFile = File(...),
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    """Production voice-intelligence workflow: quality -> ASR -> clinical extraction -> acoustic screen."""
    if not settings.voice_intelligence_enabled:
        raise HTTPException(status_code=404, detail="Voice Intelligence is not enabled.")

    _require_patient(session, patient_id, clinician)
    if not consent_confirmed:
        raise HTTPException(status_code=400, detail="Patient consent must be confirmed before recording is analysed.")
    language = (language or settings.sahara_language).strip().lower()
    if language not in {"en", "fr"}:
        raise HTTPException(status_code=422, detail="Unsupported analysis language. Choose English or French.")
    path = await _save_temp(audio)
    try:
        result = await analyse(path, language=language or settings.sahara_language)
        if not result.get("ok"):
            return VoiceIntelligenceOut(ok=False, error=result.get("error"))

        neuro = result.get("neurological_signal") or {}
        assessment = None
        if neuro:
            assessment = Assessment(
                patient_id=patient_id,
                modality="voice",
                task="voice_intelligence",
                performer=clinician.full_name or clinician.email,
                model_name=neuro.get("model_name"),
                model_version=neuro.get("model_version"),
                quality_score=neuro.get("quality_score"),
                risk_score=neuro.get("risk_score"),
                confidence=neuro.get("confidence"),
                risk_band=neuro.get("risk_band"),
                flagged=(neuro.get("risk_score") is not None and neuro.get("risk_band") in {"moderate", "elevated"}),
                narrative=result.get("clinician_summary"),
                voiced_sec=result.get("audio_duration_s"),
                n_recordings=1,
            )
            session.add(assessment)
            session.flush()
            for b in neuro.get("biomarkers", []):
                session.add(Observation(
                    assessment_id=assessment.id,
                    code=b["code"],
                    label=b["label"],
                    value=b["value"],
                    shap_contribution=b.get("shap_contribution"),
                ))

        record = VoiceIntelligenceSession(
            patient_id=patient_id,
            assessment_id=assessment.id if assessment else None,
            language=result.get("language"),
            asr_provider=result["asr_provider"],
            asr_model=result["asr_model"],
            transcript=result["transcript"],
            asr_latency_ms=result.get("asr_latency_ms"),
            audio_duration_s=result.get("audio_duration_s"),
            audio_quality_score=result.get("audio_quality_score"),
            consent_confirmed=consent_confirmed,
        )
        session.add(record)
        session.flush()

        findings = []
        for item in result.get("clinical_findings", []):
            finding = ClinicalFinding(session_id=record.id, **item)
            session.add(finding)
            findings.append(finding)
        session.commit()
        session.refresh(record)

        return VoiceIntelligenceOut(
            ok=True,
            session_id=record.id,
            transcript=record.transcript,
            language=record.language,
            asr_provider=record.asr_provider,
            asr_model=record.asr_model,
            asr_latency_ms=record.asr_latency_ms,
            audio_duration_s=record.audio_duration_s,
            audio_quality_score=record.audio_quality_score,
            consent_confirmed=record.consent_confirmed,
            clinical_findings=result.get("clinical_findings", []),
            neurological_signal=result.get("neurological_signal"),
            clinician_summary=result.get("clinician_summary"),
            safety_notes=result.get("safety_notes", []),
            created_at=record.created_at,
        )
    except HTTPException:
        raise
    except Exception as exc:
        session.rollback()
        request_id = str(uuid.uuid4())
        logger.exception("Voice Intelligence analysis failed", extra={"request_id": request_id, "patient_id": str(patient_id)})
        raise HTTPException(
            status_code=502,
            detail="Voice Intelligence analysis could not be completed. Please try again.",
            headers={"X-Request-ID": request_id},
        ) from exc
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@router.get("/patients/{patient_id}/sessions", response_model=list[VoiceIntelligenceRead])
def list_sessions(
    patient_id: uuid.UUID,
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    clinician: Clinician = Depends(get_current_clinician),
):
    _require_patient(session, patient_id, clinician)
    rows = session.exec(
        select(VoiceIntelligenceSession)
        .where(VoiceIntelligenceSession.patient_id == patient_id)
        .order_by(VoiceIntelligenceSession.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    out = []
    for row in rows:
        findings = session.exec(
            select(ClinicalFinding).where(ClinicalFinding.session_id == row.id)
        ).all()
        out.append(VoiceIntelligenceRead(
            id=row.id,
            patient_id=row.patient_id,
            assessment_id=row.assessment_id,
            language=row.language,
            asr_provider=row.asr_provider,
            asr_model=row.asr_model,
            transcript=row.transcript,
            asr_latency_ms=row.asr_latency_ms,
            audio_duration_s=row.audio_duration_s,
            audio_quality_score=row.audio_quality_score,
            consent_confirmed=row.consent_confirmed,
            findings=[ClinicalFindingRead.model_validate(f, from_attributes=True) for f in findings],
            created_at=row.created_at,
        ))
    return out
