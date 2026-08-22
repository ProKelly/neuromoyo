# Neuromoyo

AI-assisted voice screening for Parkinsonian speech patterns (NeuroVoice), rebuilt
on **FastAPI + Nuxt 3 + Supabase Postgres**, per the engineering blueprint.

This repo carries forward the working ML pipeline from the earlier "Cadence"
prototype (eGeMAPS acoustic features, logistic-regression screening model, honest
cross-corpus validation, SHAP explainability) — restructured to fit the
`AssessmentModality` architecture and given real persistence for the first time.

## What changed from the old version

| Old (Cadence) | New (Neuromoyo) |
|---|---|
| Stateless — no DB, audio scored and discarded, nothing persisted | Supabase Postgres persists `Patient` / `Assessment` / `Observation` (audio itself still never stored) |
| Flat `backend/*.py` modules | `backend/app/modalities/voice/` implementing the generic `AssessmentModality` interface (`app/modalities/base.py`) |
| Vanilla JS PWA frontend (10-language, Gradio + static site) | Nuxt 3 clinician console (English/French for now — the two languages Cameroon's own strategy prioritizes first; more languages are additive later, not a rewrite) |
| One `screen()`/`analyze_vowel()`/`analyze_ddk()` call per request, response thrown away after | Each scored assessment is saved with its biomarkers, so `GET /api/patients/{id}/assessments` gives a real longitudinal history — the basis for NeuroMonitor |
| Research/training code (`src/`) mixed into the same repo root | Moved to `research/` at the repo root, unchanged — still not imported by the deployed app |

The trained model artifact was carried over as-is (`backend/artifacts/voice_pd_v1.joblib`),
renamed to match the model-registry convention from the blueprint (`{modality}_pd_{version}`).
Its honest external validation (leave-one-dataset-out AUC ≈0.72) is unchanged — nothing about
the model itself was touched, only how the app around it is structured and persists results.

## Repo layout

```
neuromoyo/
├── backend/               FastAPI app
│   ├── app/
│   │   ├── main.py            entrypoint, CORS, DB init, model warm-up
│   │   ├── config.py          Settings (.env) incl. Supabase DATABASE_URL
│   │   ├── db.py               SQLModel engine/session
│   │   ├── models.py           Patient / Assessment / Observation (generic, not modality-specific)
│   │   ├── schemas.py          Pydantic request/response shapes
│   │   ├── routers/
│   │   │   ├── patients.py     patient CRUD + assessment history
│   │   │   └── assessments.py  voice screening endpoints (reading/vowel/ddk), persists results
│   │   └── modalities/
│   │       ├── base.py         the AssessmentModality contract every modality implements
│   │       └── voice/          migrated from the old backend/, imports fixed
│   ├── artifacts/voice_pd_v1.joblib
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               Nuxt 3 clinician console
│   ├── pages/
│   │   ├── index.vue                patient intake
│   │   └── assess/[patientId].vue   reading / vowel / ddk tasks + results + history
│   ├── components/Recorder.vue      MediaRecorder wrapper
│   ├── composables/useApi.ts        typed FastAPI client
│   ├── assets/passages.json         EN/FR reading passages (carried over from old frontend)
│   └── .env.example
└── research/               offline training/validation pipeline (unchanged, not deployed)
```

## Setup

### 1. Supabase

Create a Supabase project, then from **Project Settings → Database → Connection
string → URI**, copy the connection string (Session pooler recommended for a
long-running backend). You create the project and hold the credentials — nothing
here needs your password.

### 2. Backend

```bash
cd backend
cp .env.example .env      # paste your Supabase DATABASE_URL in here
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On first startup the app creates the `patient` / `assessment` / `observation` tables
in your Supabase database automatically (`SQLModel.metadata.create_all` — see
`app/db.py`). Once the schema stabilizes, switch to Alembic migrations instead of
relying on `create_all` for changes.

### 3. Frontend

```bash
cd frontend
cp .env.example .env      # NUXT_PUBLIC_API_BASE, defaults to localhost:8000
npm install
npm run dev
```

## API surface (V1)

| Endpoint | Purpose |
|---|---|
| `POST /api/patients` | Create a patient record |
| `GET /api/patients/{id}` | Fetch a patient |
| `GET /api/patients/{id}/assessments` | Longitudinal assessment history |
| `POST /api/assessments/voice/reading` | Reading-passage screening (produces a risk score) |
| `POST /api/assessments/voice/vowel` | Sustained-vowel phonation measurement (no risk score) |
| `POST /api/assessments/voice/ddk` | /pa-ta-ka/ rhythm measurement (no risk score) |
| `GET /api/health` | Health check |

All three voice endpoints accept `patient_id` + `audio` as multipart form data,
score it, persist an `Assessment` + its `Observation` rows, and return the result —
audio itself is discarded immediately after scoring, never stored.

## What's intentionally not here yet

- Auth (every endpoint is open — add OAuth2/JWT + role scoping before any real
  clinic pilot, per the blueprint's security section)
- Alembic migrations (using `create_all` while the schema is still moving)
- Offline-first sync (the blueprint's mobile-app design; this console is a
  connected clinician web app, not the field-capture app)
- Any modality besides voice (tapping/gait/handwriting/face are future
  `AssessmentModality` implementations, deliberately absent from V1)
- Multi-language beyond EN/FR (structure supports adding more; not done yet)
