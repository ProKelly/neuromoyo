# NEUROMOYO — Competition / Voice Intelligence Integration

## Product boundary

Voice Intelligence is a separately deployable product capability. The original neurological voice screening pipeline under `backend/app/modalities/voice/` remains intact and is not replaced by ASR or an LLM.

Production flow:

`natural speech → audio quality → canonical 16 kHz WAV → Sahara ASR → traceable clinical extraction → existing acoustic neurological screen → clinician decision-support summary`

## Feature flags

Backend:

```env
VOICE_INTELLIGENCE_ENABLED=true
SAHARA_API_URL=https://infer.voice.intron.io
SAHARA_API_KEY=<backend secret>
SAHARA_TIMEOUT_SECONDS=60
SAHARA_LANGUAGE=en
```

Frontend:

```env
NUXT_PUBLIC_VOICE_INTELLIGENCE_ENABLED=true
```

Production also requires:

```env
ENVIRONMENT=production
AUTO_CREATE_DB=false
CORS_ORIGINS=https://your-production-frontend.example
```

## API

`POST /api/voice-intelligence/analyse`

Multipart fields:

- `patient_id`
- `language` (`en` or `fr`; English mode supports natural Pidgin + English code-switching)
- `consent_confirmed` (`true` required)
- `audio`

`GET /api/voice-intelligence/patients/{patient_id}/sessions?limit=25&offset=0`

The endpoint uses the existing authenticated clinician and facility-scoping rules.

## Database

Competition-specific tables:

- `voiceintelligencesession`
- `clinicalfinding`

Apply `backend/migrations/001_voice_intelligence.sql` to an existing production database. `AUTO_CREATE_DB=true` is intended only for local/disposable environments.

The neurological screening signal is additionally recorded through the existing generic `Assessment` / `Observation` model so it participates in longitudinal reporting.

## Privacy and safety

- Raw audio is written to a temporary file only.
- Browser WebM/Opus is decoded once and converted to canonical 16 kHz mono WAV.
- Canonical audio is deleted in a `finally` block after processing.
- Patient transcript and structured findings are persisted because they are the product's clinical record; deploy the database under appropriate access controls and retention policies.
- Patient consent is required at the UI and API layers.
- Provider/model provenance is persisted with each session.
- ASR and acoustic models provide evidence/decision support; they do not autonomously diagnose Parkinson's disease.
- API/provider failures return generic client messages with request IDs; detailed exceptions remain server-side logs.

## Public competition evidence

`/benchmark` is intentionally public and presents the frozen benchmark results without requiring clinician authentication. It is a product-facing companion to the Hugging Face evidence package.

The benchmark evidence is stored under `research/hackathon/`. Raw audio and credentials are excluded.

## Detaching the competition layer

Set `VOICE_INTELLIGENCE_ENABLED=false` and `NUXT_PUBLIC_VOICE_INTELLIGENCE_ENABLED=false`.

Then remove:

```text
backend/app/voice_intelligence/
backend/app/routers/voice_intelligence.py
frontend/pages/assess/[patientId]/voice-intelligence.vue
frontend/pages/benchmark.vue
frontend/public/benchmark.json
research/hackathon/
backend/migrations/001_voice_intelligence.sql
```

Then remove the corresponding feature flags from configuration. Existing `backend/app/modalities/voice/` functionality remains independent.
