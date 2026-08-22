"""Sustained vowel /a/ analysis -- phonation voice-quality biomarkers (MEASUREMENT ONLY).

The speaker holds a steady /aaah/. We report the classic phonation markers from
eGeMAPS (jitter, shimmer, HNR, pitch stability). The original cross-corpus study
showed the sustained vowel does NOT transfer across recording channels (a negative
control) -- so this task measures and displays these values with a gentle reading,
never a Parkinson's risk score from the vowel alone. `risk_score` stays None.
"""
from __future__ import annotations

import numpy as np

from ...config import get_settings

settings = get_settings()

_J = "jitterLocal_sma3nz_amean"
_S = "shimmerLocaldB_sma3nz_amean"
_H = "HNRdBACF_sma3nz_amean"
_F = "F0semitoneFrom27.5Hz_sma3nz_stddevNorm"


def analyze_vowel(wav, sr: int | None = None) -> dict:
    import librosa
    from .egemaps import egemaps_signal
    if isinstance(wav, str) or hasattr(wav, "__fspath__"):
        from .audio_io import load_audio
        y = load_audio(wav, settings.sample_rate)
    else:
        y = np.asarray(wav, dtype=np.float32)
        if sr and sr != settings.sample_rate:
            y = librosa.resample(y, orig_sr=sr, target_sr=settings.sample_rate)
    y, _ = librosa.effects.trim(y, top_db=30)
    dur = len(y) / settings.sample_rate
    if dur < 1.0:
        return {"ok": False, "modality": "voice", "task": "vowel",
                "error": "Too short. Hold a steady 'aaah' for about 3-5 seconds."}

    vec, names = egemaps_signal(y, settings.sample_rate)
    nv = dict(zip(names, vec))

    def g(k):
        v = nv.get(k)
        return float(v) if v is not None and np.isfinite(v) else None

    jitter, shimmer, hnr, f0std = g(_J), g(_S), g(_H), g(_F)
    biomarkers = [
        {"code": _J, "label": "Jitter (pitch instability)", "value": round(jitter, 4), "shap_contribution": None}
        if jitter is not None else None,
        {"code": _S, "label": "Shimmer (dB)", "value": round(shimmer, 3), "shap_contribution": None}
        if shimmer is not None else None,
        {"code": _H, "label": "Harmonics-to-noise (dB)", "value": round(hnr, 2), "shap_contribution": None}
        if hnr is not None else None,
        {"code": _F, "label": "Pitch stability", "value": round(f0std, 3), "shap_contribution": None}
        if f0std is not None else None,
    ]
    biomarkers = [b for b in biomarkers if b is not None]

    return {
        "ok": True,
        "modality": "voice",
        "task": "vowel",
        "quality_score": round(min(1.0, dur / 5.0), 2),
        "risk_score": None,  # measurement-only task, never scored for PD risk on its own
        "duration": round(float(dur), 1),
        "biomarkers": biomarkers,
        "narrative": _reading(hnr, jitter, shimmer),
    }


def _reading(hnr, jitter, shimmer) -> str:
    concerns = []
    if hnr is not None and hnr < 7:
        concerns.append("the voice sounded a little breathy or noisy (lower harmonics-to-noise)")
    if jitter is not None and jitter > 0.03:
        concerns.append("pitch was slightly unsteady (raised jitter)")
    if shimmer is not None and shimmer > 1.3:
        concerns.append("loudness was slightly unsteady (raised shimmer)")
    if not concerns:
        return ("The sustained vowel was clear and steady. Reduced voice clarity or an unsteady "
                "vowel can accompany Parkinsonian speech, and this did not stand out.")
    return ("On the sustained vowel, " + "; ".join(concerns) + ". These can reflect the recording "
            "conditions as much as the voice, so they're reported as measurements only, not a verdict.")
