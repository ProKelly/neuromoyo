from __future__ import annotations

from .base import ASRProvider
from .sahara import SaharaProvider


def get_provider(name: str) -> ASRProvider:
    providers = {
        "sahara": SaharaProvider(),
        "intron_sahara": SaharaProvider(),
    }
    try:
        return providers[name.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported ASR provider: {name}") from exc
