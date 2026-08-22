"""Serving-only model access for the voice modality.

The training pipeline (cross-corpus validation, DANN experiments, etc.) lives in
`research/` at the repo root -- it is NOT imported by the deployed app. This module
only loads the frozen artifact and scores feature vectors against it.

Model registry convention (blueprint §4.2): `{modality}_pd_{version}`. This is
currently `voice_pd_v1`, trained on pooled Italian + MDVR-KCL reading recordings,
honest external (leave-one-dataset-out) AUC ~0.72. See research/RESULTS.md
(carry over from the original project) for the full validation writeup.
"""
from __future__ import annotations

import numpy as np
import joblib

from ...config import ARTIFACTS_DIR

MODEL_NAME = "voice_pd"
MODEL_VERSION = "1"
MODEL_PATH = ARTIFACTS_DIR / f"{MODEL_NAME}_v{MODEL_VERSION}.joblib"

_bundle_cache = None


def load_model():
    global _bundle_cache
    if _bundle_cache is None:
        _bundle_cache = joblib.load(MODEL_PATH)
    return _bundle_cache


def predict_proba_from_features(feats: dict, bundle=None) -> float:
    """feats: dict of ALL acoustic features (egemaps output). Returns P(PD)."""
    bundle = bundle or load_model()
    names = bundle["feature_names"]
    x = np.array([[feats[n] for n in names]], dtype=float)
    return float(bundle["pipeline"].predict_proba(x)[0, 1])
