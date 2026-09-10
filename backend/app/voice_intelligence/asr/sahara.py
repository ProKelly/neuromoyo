from __future__ import annotations

import time
import uuid
from pathlib import Path
import httpx

from ...config import get_settings
from ..schemas import ASRResult
from .base import ASRProvider

settings = get_settings()


class SaharaProvider(ASRProvider):
    name = "intron_sahara"
    model = "sahara"

    async def transcribe(self, audio: str | Path, language: str = "en") -> ASRResult:
        if not settings.sahara_api_key:
            raise RuntimeError("SAHARA_API_KEY is not configured on the backend.")

        path = Path(audio)
        request_id = str(uuid.uuid4())
        started = time.perf_counter()

        data = {
            "audio_file_name": path.name,
            "use_language_asr_input": language or settings.sahara_language,
        }
        # The provider supports sync file upload and a maximum duration of 120s.
        with path.open("rb") as fh:
            files = {"audio_file_blob": (path.name, fh, "audio/wav")}
            timeout = httpx.Timeout(settings.sahara_timeout_seconds, connect=15.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    settings.sahara_api_url.rstrip("/") + "/file/v1/upload/sync",
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {settings.sahara_api_key}", "X-Request-ID": request_id},
                )

                payload = response.json()
                if response.status_code == 503:
                    file_id = payload.get("data", {}).get("file_id") if isinstance(payload, dict) else None
                    if file_id:
                        payload = await self._poll_status(client, file_id)
                    else:
                        raise RuntimeError(f"Sahara queued the request without a file id: {payload}")
                elif response.status_code >= 400:
                    detail = response.text[-800:]
                    raise RuntimeError(f"Sahara transcription failed ({response.status_code}): {detail}")

        transcript = _extract_transcript(payload).strip()
        if not transcript:
            raise RuntimeError("Sahara returned no transcript.")

        elapsed = (time.perf_counter() - started) * 1000
        return ASRResult(
            provider=self.name,
            model=self.model,
            transcript=transcript,
            language=language,
            latency_ms=round(elapsed, 1),
            audio_duration_s=0.0,
            request_id=request_id,
        )


    async def _poll_status(self, client: httpx.AsyncClient, file_id: str) -> dict:
        deadline = time.perf_counter() + settings.sahara_timeout_seconds
        url = settings.sahara_api_url.rstrip("/") + f"/file/v1/status/{file_id}"
        while time.perf_counter() < deadline:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {settings.sahara_api_key}"},
            )
            if response.status_code >= 400:
                raise RuntimeError(f"Sahara status check failed ({response.status_code}): {response.text[-600:]}")
            payload = response.json()
            data = payload.get("data", {}) if isinstance(payload, dict) else {}
            status = data.get("processing_status")
            if status == "FILE_TRANSCRIBED":
                return payload
            if status == "FILE_PROCESSING_FAILED":
                raise RuntimeError("Sahara failed while processing the audio file.")
            await __import__("asyncio").sleep(2.0)
        raise RuntimeError("Sahara transcription timed out while processing the audio file.")


def _extract_transcript(payload: object) -> str:
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return ""

    for key in ("audio_transcript", "transcription", "transcript", "text"):
        value = payload.get(key)
        if isinstance(value, str):
            return value

    # Keep this tolerant of minor API response-shape changes.
    for key in ("data", "result", "output"):
        value = payload.get(key)
        if isinstance(value, dict):
            text = _extract_transcript(value)
            if text:
                return text
        if isinstance(value, list):
            for item in value:
                text = _extract_transcript(item)
                if text:
                    return text
    return ""
