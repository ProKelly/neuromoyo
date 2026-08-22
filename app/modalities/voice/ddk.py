"""Diadochokinetic (DDK) analysis -- the classic bedside PD motor-speech test.

The speaker repeats /pa-ta-ka/ as fast and steadily as possible. We measure two
transparent, model-free quantities from the amplitude envelope:
  * syllable_rate  - syllables per second (PD tends to be SLOWER)
  * regularity     - 1 - CV of inter-syllable intervals (PD tends to be MORE IRREGULAR)
These are physical measurements with published normative ranges, not a trained
classifier -- honest to report on any device. `risk_score` stays None.
"""
from __future__ import annotations

import numpy as np

from ...config import get_settings

settings = get_settings()
RATE_TYPICAL = (5.0, 7.0)


def analyze_ddk(wav, sr: int | None = None) -> dict:
    import librosa
    SR = settings.sample_rate
    if isinstance(wav, (str,)) or hasattr(wav, "__fspath__"):
        from .audio_io import load_audio
        y = load_audio(wav, SR)
    else:
        y = np.asarray(wav, dtype=np.float32)
        if sr and sr != SR:
            y = librosa.resample(y, orig_sr=sr, target_sr=SR)
    y, _ = librosa.effects.trim(y, top_db=30)
    dur = len(y) / SR
    if dur < 1.5:
        return {"ok": False, "modality": "voice", "task": "ddk",
                "error": "Too short. Say 'pa-ta-ka' repeatedly for about 5 seconds."}

    hop = int(0.01 * SR)
    rms = librosa.feature.rms(y=y, frame_length=int(0.025 * SR), hop_length=hop)[0]
    env = rms / (rms.max() + 1e-9)
    from scipy.ndimage import uniform_filter1d
    env = uniform_filter1d(env, size=3)
    fps = SR / hop

    from scipy.signal import find_peaks
    peaks, _ = find_peaks(env, distance=int(0.12 * fps), prominence=0.08)
    n = int(len(peaks))
    rate = n / dur if dur > 0 else 0.0

    cv = None
    if n >= 3:
        intervals = np.diff(peaks) / fps
        cv = float(np.std(intervals) / (np.mean(intervals) + 1e-9))
    regularity = round(float(max(0.0, 1.0 - cv)), 2) if cv is not None else None

    biomarkers = [
        {"code": "ddk_syllable_rate", "label": "Syllable rate (/sec)", "value": round(float(rate), 2), "shap_contribution": None},
    ]
    if regularity is not None:
        biomarkers.append({"code": "ddk_regularity", "label": "Rhythm regularity", "value": regularity, "shap_contribution": None})

    return {
        "ok": True,
        "modality": "voice",
        "task": "ddk",
        "quality_score": round(min(1.0, dur / 5.0), 2),
        "risk_score": None,  # model-free measurement task, never scored for PD risk on its own
        "syllable_rate": round(float(rate), 2),
        "n_syllables": n,
        "duration": round(float(dur), 1),
        "interval_cv": round(cv, 3) if cv is not None else None,
        "regularity": regularity,
        "rate_typical": list(RATE_TYPICAL),
        "biomarkers": biomarkers,
        "narrative": _reading(rate, regularity),
    }


def _reading(rate: float, regularity) -> str:
    lo, hi = RATE_TYPICAL
    if rate >= lo and (regularity is None or regularity >= 0.7):
        return ("Repetition rate and rhythm are within a typical adult range. Slowed or uneven "
                "/pa-ta-ka/ can be a sign of Parkinsonian speech, and this did not stand out.")
    parts = []
    if rate < lo:
        parts.append(f"the repetition rate ({rate:.1f}/sec) is below the typical {lo:.0f}-{hi:.0f}/sec range")
    if regularity is not None and regularity < 0.7:
        parts.append("the rhythm was somewhat uneven")
    body = " and ".join(parts) if parts else "some patterns were slightly outside the typical range"
    return (f"On this task {body}. Slowed or irregular rapid speech can accompany Parkinson's, "
            "but this single task cannot diagnose anything on its own.")
