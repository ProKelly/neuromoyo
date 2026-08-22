"""The AssessmentModality contract (blueprint §4.1).

Every modality -- voice today, tapping/spiral/gait/face later -- must produce this
standardized shape. The API layer and (eventually) the fusion engine consume this
and don't need to know how a given modality computed its score. Add a modality by
adding a new class that implements `run()`, not by touching this file or the DB
schema.
"""
from __future__ import annotations

from typing import TypedDict


class Biomarker(TypedDict):
    code: str
    label: str
    value: float
    shap_contribution: float | None


class ModalityResult(TypedDict, total=False):
    ok: bool
    error: str | None
    modality: str
    task: str
    biomarkers: list[Biomarker]
    model_name: str
    model_version: str
    quality_score: float | None
    risk_score: float | None
    confidence: float | None
    risk_band: str | None
    flagged: bool | None
    narrative: str | None
    voiced_sec: float | None
    n_windows: int | None
    n_recordings: int | None
    disclaimer: str
