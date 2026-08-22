from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from ..db import get_session
from ..models import Assessment, Observation, Patient
from ..schemas import ScreenResultOut
from ..modalities.voice import screen as voice_screen
from ..modalities.voice import vowel as voice_vowel
from ..modalities.voice import ddk as voice_ddk

router = APIRouter(prefix="/api/assessments/voice", tags=["assessments:voice"])


async def _to_temp(up: UploadFile) -> str | None:
    data = await up.read()
    if not data:
        return None
    suffix = Path(up.filename or "clip.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        return tmp.name


def _cleanup(paths: list[str]) -> None:
    for p in paths:
        try:
            os.remove(p)
        except OSError:
            pass


def _persist(session: Session, patient_id: uuid.UUID, performer: str | None, result: dict) -> Assessment | None:
    """Audio itself is never stored (deleted after scoring, per the original design's
    privacy stance) -- only the derived biomarkers and scores are persisted."""
    if not result.get("ok"):
        return None
    assessment = Assessment(
        patient_id=patient_id,
        modality=result["modality"],
        task=result["task"],
        performer=performer,
        model_name=result.get("model_name"),
        model_version=result.get("model_version"),
        quality_score=result.get("quality_score"),
        risk_score=result.get("risk_score"),
        confidence=result.get("confidence"),
        risk_band=result.get("risk_band"),
        flagged=result.get("flagged"),
        narrative=result.get("narrative"),
        voiced_sec=result.get("voiced_sec"),
        n_windows=result.get("n_windows"),
        n_recordings=result.get("n_recordings"),
    )
    session.add(assessment)
    session.flush()  # get assessment.id before adding observations

    for b in result.get("biomarkers", []):
        session.add(Observation(
            assessment_id=assessment.id,
            code=b["code"], label=b["label"], value=b["value"],
            shap_contribution=b.get("shap_contribution"),
        ))
    session.commit()
    session.refresh(assessment)
    return assessment


def _require_patient(session: Session, patient_id: uuid.UUID) -> Patient:
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/reading", response_model=ScreenResultOut)
async def screen_reading(
    patient_id: uuid.UUID = Form(...),
    performer: str | None = Form(None),
    audio: list[UploadFile] = File(...),
    session: Session = Depends(get_session),
):
    """Reading-passage task -- the only task that produces a risk_score (the ML model)."""
    _require_patient(session, patient_id)
    paths = []
    try:
        for up in audio:
            p = await _to_temp(up)
            if p:
                paths.append(p)
        if not paths:
            raise HTTPException(status_code=400, detail="Empty audio upload.")
        result = voice_screen.screen(paths[0]) if len(paths) == 1 else voice_screen.screen_many(paths)
        assessment = _persist(session, patient_id, performer, result)
    except HTTPException:
        raise
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
    finally:
        _cleanup(paths)
    return ScreenResultOut(
        ok=result["ok"], error=result.get("error"),
        assessment_id=assessment.id if assessment else None,
        modality=result.get("modality"), task=result.get("task"),
        risk_score=result.get("risk_score"), threshold=result.get("threshold"),
        flagged=result.get("flagged"), risk_band=result.get("risk_band"),
        confidence=result.get("confidence"), quality_score=result.get("quality_score"),
        voiced_sec=result.get("voiced_sec"), n_windows=result.get("n_windows"),
        n_recordings=result.get("n_recordings"), narrative=result.get("narrative"),
        biomarkers=result.get("biomarkers", []), disclaimer=result.get("disclaimer"),
    )


@router.post("/vowel", response_model=ScreenResultOut)
async def screen_vowel(
    patient_id: uuid.UUID = Form(...),
    performer: str | None = Form(None),
    audio: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """Sustained-vowel task -- measurement only, risk_score is always None."""
    _require_patient(session, patient_id)
    p = await _to_temp(audio)
    if not p:
        raise HTTPException(status_code=400, detail="Empty audio upload.")
    try:
        result = voice_vowel.analyze_vowel(p)
        assessment = _persist(session, patient_id, performer, result)
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Vowel analysis failed: {e}")
    finally:
        _cleanup([p])
    return ScreenResultOut(
        ok=result["ok"], error=result.get("error"),
        assessment_id=assessment.id if assessment else None,
        modality=result.get("modality"), task=result.get("task"),
        risk_score=result.get("risk_score"), quality_score=result.get("quality_score"),
        narrative=result.get("narrative"), biomarkers=result.get("biomarkers", []),
    )


@router.post("/ddk", response_model=ScreenResultOut)
async def screen_ddk(
    patient_id: uuid.UUID = Form(...),
    performer: str | None = Form(None),
    audio: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """Diadochokinetic (/pa-ta-ka/) task -- measurement only, risk_score is always None."""
    _require_patient(session, patient_id)
    p = await _to_temp(audio)
    if not p:
        raise HTTPException(status_code=400, detail="Empty audio upload.")
    try:
        result = voice_ddk.analyze_ddk(p)
        assessment = _persist(session, patient_id, performer, result)
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"DDK analysis failed: {e}")
    finally:
        _cleanup([p])
    return ScreenResultOut(
        ok=result["ok"], error=result.get("error"),
        assessment_id=assessment.id if assessment else None,
        modality=result.get("modality"), task=result.get("task"),
        risk_score=result.get("risk_score"), quality_score=result.get("quality_score"),
        narrative=result.get("narrative"), biomarkers=result.get("biomarkers", []),
    )
