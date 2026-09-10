from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from ..schemas import ASRResult


class ASRProvider(ABC):
    name: str
    model: str

    @abstractmethod
    async def transcribe(self, audio: str | Path, language: str = "en") -> ASRResult:
        raise NotImplementedError
