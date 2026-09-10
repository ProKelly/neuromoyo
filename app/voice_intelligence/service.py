from __future__ import annotations

import tempfile
from pathlib import Path

import soundfile as sf

from .audio.quality import inspect
from .asr.registry import get_provider
from .clinical.extractor import extract
from .clinical.summary import build_summary
from .safety.policy import SAFETY_NOTES
from ..modalities.voice import screen as voice_screen


async def analyse(audio_path: str | Path, language: str = "en") -> dict:
    path = Path(audio_path)
    y, quality = inspect(path)
    if not quality.ok:
        return {"ok": False, "error": quality.message}

    # Normalise browser audio once to a canonical 16 kHz mono WAV. This avoids
    # sending WebM/Opus with a misleading MIME type to the ASR provider and
    # guarantees that both ASR and the neurological pipeline analyse the same
    # signal. The canonical file is deleted immediately after processing.
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        canonical_path = Path(tmp.name)
    try:
        sf.write(canonical_path, y, 16_000, subtype="PCM_16")

        provider = get_provider("sahara")
        asr = await provider.transcribe(canonical_path, language=language)
        asr.audio_duration_s = quality.duration_s

        findings = extract(asr.transcript)

        # Existing neurological acoustic pipeline remains independent of ASR.
        neuro = voice_screen.screen(canonical_path)

        neuro_signal = None
        if neuro.get("ok"):
            neuro_signal = {
                "risk_score": neuro.get("risk_score"),
                "risk_band": neuro.get("risk_band"),
                "confidence": neuro.get("confidence"),
                "quality_score": neuro.get("quality_score"),
                "biomarkers": neuro.get("biomarkers", []),
                "model_name": neuro.get("model_name"),
                "model_version": neuro.get("model_version"),
            }

        return {
            "ok": True,
            "transcript": asr.transcript,
            "language": language,
            "asr_provider": asr.provider,
            "asr_model": asr.model,
            "asr_latency_ms": asr.latency_ms,
            "audio_duration_s": quality.duration_s,
            "audio_quality_score": quality.score,
            "clinical_findings": findings,
            "neurological_signal": neuro_signal,
            "clinician_summary": build_summary(findings, neuro_signal),
            "safety_notes": SAFETY_NOTES,
        }
    finally:
        canonical_path.unlink(missing_ok=True)
