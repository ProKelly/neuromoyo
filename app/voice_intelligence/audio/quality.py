from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np

from ...config import get_settings
from ...modalities.voice.audio_io import load_audio

settings = get_settings()


@dataclass
class AudioQuality:
    ok: bool
    message: str
    duration_s: float
    voiced_s: float
    clipping_ratio: float
    score: float


def inspect(path: str | Path) -> tuple[np.ndarray, AudioQuality]:
    import librosa

    y = load_audio(path, settings.sample_rate)
    if y.size == 0:
        return y, AudioQuality(False, "The recording is empty.", 0, 0, 1, 0)

    duration = float(len(y) / settings.sample_rate)
    intervals = librosa.effects.split(y, top_db=30)
    voiced = float(sum(b - a for a, b in intervals) / settings.sample_rate) if len(intervals) else 0.0
    clipping = float(np.mean(np.abs(y) >= 0.985))

    if duration < 5:
        return y, AudioQuality(False, "Recording is too short. Please speak for at least 5 seconds.", duration, voiced, clipping, 0.0)
    if duration > 120:
        return y, AudioQuality(False, "Recording exceeds the 120-second processing limit.", duration, voiced, clipping, 0.0)
    if clipping > 0.02:
        return y, AudioQuality(False, "The recording is clipping. Move slightly farther from the microphone and try again.", duration, voiced, clipping, 0.0)
    if voiced < 3:
        return y, AudioQuality(False, "Too little clear speech was detected. Please record again in a quieter place.", duration, voiced, clipping, 0.0)

    speech_ratio = min(1.0, voiced / max(duration, 1.0))
    duration_score = min(1.0, duration / 20.0)
    clip_score = max(0.0, 1.0 - clipping / 0.02)
    score = round(0.55 * speech_ratio + 0.35 * duration_score + 0.10 * clip_score, 2)

    return y, AudioQuality(True, "", duration, voiced, clipping, score)
