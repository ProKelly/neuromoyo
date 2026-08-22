"""Shared audio loading, robust to whatever codec the browser actually sends.

`librosa`/`soundfile` can only decode formats libsndfile understands natively
(WAV, FLAC, OGG-Vorbis...). As of librosa 1.0, the old automatic fallback to
`audioread`/ffmpeg for other containers (webm/opus, mp4/aac, mp3...) is gone --
so a MediaRecorder-produced `audio/webm` clip (the browser's default) fails with
a bare "Format not recognised" the moment it hits `librosa.load`.

This module tries the fast path first (soundfile, no subprocess) and transcodes
via ffmpeg only when that fails, so WAV/FLAC uploads stay fast and everything
else (webm, ogg/opus, mp4/aac, mp3, ...) still works. Requires `ffmpeg` on PATH --
already installed in the Docker image (see Dockerfile); for local `uvicorn`
dev, install it separately (e.g. `apt install ffmpeg` / `brew install ffmpeg`).
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np


def load_audio(path: str | Path, target_sr: int) -> np.ndarray:
    """Return a mono float32 array at `target_sr`, decoding via ffmpeg if needed."""
    import librosa
    try:
        y, _ = librosa.load(str(path), sr=target_sr, mono=True)
        return y
    except Exception:
        wav_path = _transcode_to_wav(path, target_sr)
        try:
            y, _ = librosa.load(str(wav_path), sr=target_sr, mono=True)
            return y
        finally:
            Path(wav_path).unlink(missing_ok=True)


def _transcode_to_wav(path: str | Path, target_sr: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        out_path = tmp.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(path), "-ac", "1", "-ar", str(target_sr), out_path],
            check=True, capture_output=True, timeout=30,
        )
    except FileNotFoundError as e:
        raise RuntimeError(
            "ffmpeg is not installed or not on PATH. It's required to decode browser-recorded "
            "audio (webm/opus). Install it (e.g. `apt install ffmpeg` or `brew install ffmpeg`) "
            "and restart the backend."
        ) from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not decode audio: {e.stderr.decode(errors='replace')[-500:]}") from e
    return out_path
