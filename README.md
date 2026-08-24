# Neuromoyo

AI-assisted voice screening and longitudinal monitoring for Parkinsonian speech
patterns (NeuroVoice), built on **FastAPI + Nuxt 3 + Tailwind v4 + Supabase
(Postgres + Auth)**.

This repo carries forward the working ML pipeline from the earlier "Cadence"
prototype (eGeMAPS acoustic features, logistic-regression screening model, honest
cross-corpus validation, SHAP explainability) — restructured into a real
clinician console: authenticated, facility-scoped patient records; a dashboard
for monitoring a caseload rather than one patient at a time; a synthesized
cross-task report a neurologist can act on; and an English/French interface.

## What this actually does, and doesn't, solve

Worth being explicit about, since it shapes every design decision below.

**The real gap it targets**: in a setting where specialist neurological care is
scarce, a clinician typically sees a patient once, for 20–30 minutes, and has to
reconstruct weeks of symptom change from "the shaking has gotten worse."
NeuroVoice doesn't replace that visit — it gives the *primary-care* touchpoint
(a nurse, a CHW, a first appointment) a structured, repeatable measurement taken
in under a minute with a phone, so a referral to a neurologist arrives with
*objective trend data* attached instead of a patient's memory of the last month.
The dashboard and report are both built around that: not "who has Parkinson's"
(this system cannot say that), but "whose numbers have moved since last time,"
and "here's the combined picture across every task this patient has completed,
with a plain-language recommendation and the specific measurements it's based
on."

**What it is not**: a diagnostic tool. The underlying model's honest external
validation is ≈0.72 AUC on cross-corpus data — informative, not remotely
diagnostic-grade. Every screen band, every dashboard flag, and every report
recommendation says "further evaluation recommended" or "refer to a
neurologist," never a diagnosis — enforced structurally (see
`app/reporting.py`'s recommendation text, `screen.py`'s `DISCLAIMER`, and
`PatientReport.disclaimer` rendered on every generated report), not just a UI
convention that's easy to forget.

**What would make the pain-point case stronger before a real pilot**: this still
needs the clinical validation loop of correlating screening output against
clinician UPDRS-style assessments on the same patients before "elevated risk"
should influence a single real referral decision. Right now it's a
well-engineered *instrument*, not yet a *validated* one.

## Repo layout

```
neuromoyo/
├── backend/               FastAPI app
│   ├── app/
│   │   ├── main.py             entrypoint, CORS, DB init, model warm-up
│   │   ├── config.py           Settings (.env): Supabase URL/DB, JWT secret
│   │   ├── db.py                SQLModel engine/session (lazy — boots without DB configured)
│   │   ├── auth.py             verifies Supabase Auth tokens (ES256/JWKS or HS256 legacy),
│   │   │                       auto-provisions/loads the matching Clinician
│   │   ├── models.py           Clinician / Patient / Assessment / Observation
│   │   ├── schemas.py          Pydantic request/response shapes, incl. PatientReport
│   │   ├── reporting.py        builds the cross-task report: trend detection,
│   │   │                       rule-based recommendation tier, supporting findings
│   │   ├── routers/
│   │   │   ├── patients.py     patient CRUD, facility auto-assignment, report endpoint
│   │   │   ├── assessments.py  voice screening endpoints (reading/vowel/ddk), persists results
│   │   │   └── clinicians.py   /me + admin-only facility/role assignment
│   │   └── modalities/
│   │       ├── base.py         the AssessmentModality contract every modality implements
│   │       └── voice/          screen/vowel/ddk/egemaps/explain + audio_io.py (ffmpeg fallback
│   │                           for browser-recorded webm/opus, which soundfile can't read natively)
│   ├── artifacts/voice_pd_v1.joblib
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               Nuxt 3 + Tailwind v4 clinician console
│   ├── pages/
│   │   ├── welcome.vue                   public landing page (signed-out default)
│   │   ├── login.vue                     Supabase Auth email/password sign-in
│   │   ├── index.vue                     dashboard: roster, search/filter, stats, mini-trends
│   │   ├── patients/new.vue              patient intake (facility auto-assigned, not typed)
│   │   └── assess/[patientId]/
│   │       ├── ../[patientId].vue        parent layout: header + section nav + <NuxtPage/>
│   │       ├── index.vue                 overview: latest status + action cards
│   │       ├── record.vue                reading / vowel / ddk recording tasks
│   │       ├── history.vue               assessment list + biomarker trends
│   │       ├── report.vue                cross-task report + "Download as PDF"
│   │       └── details.vue               patient details, view/edit
│   ├── components/
│   │   ├── Logo.vue / MascotLogo.vue   wordmark + mascot, both built from the same
│   │   │                               waveform motif as everything below
│   │   ├── Recorder.vue                MediaRecorder wrapper with a LIVE waveform (Web Audio)
│   │   ├── RiskGauge.vue               arc gauge for a single result's risk score
│   │   ├── TrendChart.vue              hand-drawn SVG line for any point series over time
│   │   └── LanguageToggle.vue          EN/FR switch for the console's own UI text
│   ├── composables/
│   │   ├── useApi.ts            typed FastAPI client, attaches the Supabase bearer token
│   │   ├── useAuth.ts           thin reactive wrapper over Supabase Auth
│   │   └── useI18n.ts           lightweight EN/FR dictionary + toggle for UI chrome
│   ├── middleware/auth.global.ts   redirects signed-out users to /welcome
│   ├── plugins/supabase.client.ts  Supabase JS client (browser-only)
│   ├── assets/css/main.css      Tailwind v4 entry + design tokens (@theme) + print rules
│   ├── assets/passages.json     EN/FR reading passages (per-patient recording language)
│   └── .env.example
└── research/               offline training/validation pipeline (unchanged, not deployed)
```

### Design

Palette and type are Tailwind v4 `@theme` tokens in `frontend/assets/css/main.css`
— deep teal for trust/actions, gold/rust reserved only for moderate/elevated risk
states, Fraunces for display headings, Inter for body/UI, IBM Plex Mono for
biomarker values. Deliberately not the cream+terracotta or near-black+neon
defaults — this is a clinical tool for health workers on ordinary Android
screens, not a marketing page.

The signature visual element is functional, not decorative, and it's the same
idea repeated across the app: `Recorder.vue` draws a *live* waveform from the
actual microphone signal via Web Audio's `AnalyserNode` while recording, so a
health worker gets real confirmation the mic is picking up voice.
`RiskGauge.vue` and `TrendChart.vue` echo the same waveform-bar language for a
single result and for change over time; `Logo.vue`/`MascotLogo.vue` use the
same motif again. Brand mark, live recording feedback, single-result gauge, and
longitudinal trend chart all read as one visual idea rather than four unrelated
decisions.

**Patient page structure**: the old design was one page with six inline tab
buttons. It's now a parent layout (`assess/[patientId].vue`, fetches the
patient + current clinician once and shares them via `provide`/`inject`) with
five focused child routes — Overview, Record, History & Trends, Report,
Details — each with its own URL. `record.vue` keeps reading/vowel/ddk as
*internal* tabs, since administering today's tests genuinely is one workflow;
the others are separate destinations because they're separate concerns (act on
a result vs. review history vs. generate something to hand off).

**Two different "language" concepts, don't confuse them**: `LanguageToggle.vue`
/ `useI18n.ts` switch the *console's own interface text* between English and
French, via `useState('i18n:locale', ...)` + `localStorage`. A patient's
`language` field (set at intake) independently selects which language the
*reading passage* is shown in — a French-speaking clinician can screen an
English-speaking patient, or vice versa.

## The cross-task report

`GET /api/patients/{id}/report` (`app/reporting.py`) synthesizes everything a
patient has completed — reading, sustained vowel, /pa-ta-ka/ — into one
document, rather than a neurologist having to piece together three separate
task histories:

- **Task completion summary**: count and most recent date per task, with the
  latest risk band for reading (the only risk-scored task).
- **Reading risk trend**: the full point series plus a direction call
  (increasing/decreasing/stable/insufficient data) — computed by comparing the
  mean of the first half of the series to the second half, against a noise
  floor, not a raw first-vs-last comparison that a single outlier could swing.
- **Biomarker trends across all tasks**: any measurement code seen at least
  twice, from any task, with its own direction.
- **Supporting findings**: threshold checks against the *measurement-only*
  tasks (vowel jitter/shimmer/HNR, DDK rate/regularity) — these tasks never
  produce a risk score on their own (see `vowel.py`/`ddk.py`), but they still
  contribute corroborating evidence to the combined report.
- **Recommendation tier** (`priority_referral` / `monitor` / `routine` /
  `insufficient_data`): rule-based, not a second model — every branch in
  `reporting.py` traces to a specific stated measurement or trend, deliberately
  kept inspectable rather than another black box on top of the first one. This
  is the same explainability requirement the single-assessment SHAP breakdown
  was already built around, just applied at the report level.

The frontend report page (`assess/[patientId]/report.vue`) renders this and
offers **"Download as PDF"**, which is just `window.print()` with print CSS
(global rules in `main.css` hide the app chrome; `print:hidden` hides the
page's own buttons) — no PDF library, so the PDF is pixel-identical to what's
on screen and never drifts out of sync with the web view.

## Setup

### 1. Supabase

Create a Supabase project. You'll need:

- **Database → Connection string → URI** (Session pooler recommended) — `DATABASE_URL`
- **Authentication → Sign-in methods**: enable Email, and create clinician accounts
  under **Authentication → Users → Add user** (no public self-signup — accounts
  are provisioned by an admin)
- **Project Settings → API → Project URL and `anon public` key** — `SUPABASE_URL`
  (both backend and frontend need this) and the frontend's `NUXT_PUBLIC_SUPABASE_ANON_KEY`

That's it for most projects. Backend token verification (`app/auth.py`) checks
the token's own header to decide how to verify it:

- **Most Supabase projects today** sign tokens with **ES256** (asymmetric keys)
  and publish the public key at `<SUPABASE_URL>/auth/v1/.well-known/jwks.json`
  — verified automatically from `SUPABASE_URL` alone, no secret needed. This is
  why `SUPABASE_JWT_SECRET` is optional in `.env.example`.
- **Older projects**, or ones with legacy signing explicitly enabled, sign with
  a single HS256 shared secret instead. Only if `auth.py` reports "This project
  signs tokens with HS256 but SUPABASE_JWT_SECRET is not configured" do you
  need **Project Settings → API → JWT Settings → Legacy JWT Secret** in `.env`.
- A 401 saying `the specified alg value is not allowed` means the token's
  signing method doesn't match what got configured — almost always `SUPABASE_URL`
  is missing/wrong (JWKS verification never got attempted), not that an HS256
  secret is wrong.

The very first person who logs in is auto-provisioned as `role="clinician"`
with **no facility**, which means they can see and create zero patients (safe
default — see `_assert_can_access` and `create_patient` in `routers/patients.py`,
both apply the same rule so a newly-provisioned account can't silently create a
patient it then can't see). Promote yourself to admin once, directly in the
Supabase table editor (`clinician.role = 'admin'`) — from there, assign
facilities/roles to everyone else via `PATCH /api/clinicians/{id}`.

**Facility assignment is never free-typed by a regular clinician** — it's
assigned server-side from their own `Clinician.facility` at patient-creation
time, so there's no string for a typo to corrupt into an invisible patient. An
admin, not being tied to one facility, still specifies one explicitly, but from
a picker (`GET /api/patients/facilities`) fed by facilities already in use, not
a blank text field. Reassigning an *existing* patient's facility
(`PATCH .../facility`) is admin-only for the same reason: a clinician editing
that field on their own patient would be a way to move it into or out of their
own visibility.

### 2. Backend

Requires **ffmpeg** on PATH (`apt install ffmpeg` / `brew install ffmpeg`) —
browsers record audio as webm/opus, which `librosa`/`soundfile` can't decode
natively as of librosa 1.0; the backend shells out to ffmpeg to transcode it
first (see `app/modalities/voice/audio_io.py`). Already installed in the Docker
image; a separate step for local `uvicorn` dev.

```bash
cd backend
cp .env.example .env      # DATABASE_URL, SUPABASE_URL, etc.
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

After editing `.env`, **restart** the process — settings are only read once at
startup (`--reload` watches Python files, not `.env`). On first startup the app
creates the `clinician` / `patient` / `assessment` / `observation` tables in
Supabase automatically (`SQLModel.metadata.create_all` — see `app/db.py`). Once
the schema stabilizes, switch to Alembic migrations instead of relying on
`create_all` for changes.

### 3. Frontend

```bash
cd frontend
cp .env.example .env      # NUXT_PUBLIC_API_BASE, NUXT_PUBLIC_SUPABASE_URL, NUXT_PUBLIC_SUPABASE_ANON_KEY
npm install
npm run dev
```

## API surface

Every route below (except `/api/health`) requires `Authorization: Bearer
<token>` from a Supabase Auth session — see `app/auth.py`.

| Endpoint | Purpose |
|---|---|
| `GET /api/clinicians/me` | Who am I, what facility/role am I scoped to (auto-provisions on first login) |
| `GET /api/clinicians` | Admin-only: list all clinicians |
| `PATCH /api/clinicians/{id}` | Admin-only: assign a clinician's facility/role |
| `POST /api/patients` | Create a patient — `facility` assigned server-side from the clinician's own record; an admin must specify one explicitly |
| `GET /api/patients` | List patients — facility-scoped for a clinician, all for an admin |
| `GET /api/patients/{id}` | Fetch a patient (404 if outside your facility) |
| `PATCH /api/patients/{id}` | Edit a patient's own details (any field except `facility`, admin-only) |
| `GET /api/patients/facilities` | Distinct facility names in use — feeds the admin intake form's picker |
| `GET /api/patients/{id}/assessments` | Longitudinal assessment history — feeds History & Trends |
| `GET /api/patients/{id}/report` | Synthesized cross-task report — see "The cross-task report" above |
| `POST /api/assessments/voice/reading` | Reading-passage screening (produces a risk score) |
| `POST /api/assessments/voice/vowel` | Sustained-vowel phonation measurement (no risk score) |
| `POST /api/assessments/voice/ddk` | /pa-ta-ka/ rhythm measurement (no risk score) |
| `GET /api/health` | Health check (no auth) |

All three voice endpoints accept `patient_id` + `audio` as multipart form data,
score it, persist an `Assessment` + its `Observation` rows (attributed to the
authenticated clinician), and return the result — audio itself is discarded
immediately after scoring, never stored.

## What's intentionally not here yet

- Alembic migrations (using `create_all` while the schema is still moving)
- Offline-first sync (a future mobile field-capture app; this console is a
  connected clinician web app)
- Any modality besides voice (tapping/gait/handwriting/face are future
  `AssessmentModality` implementations, deliberately absent from V1)
- Multi-language beyond EN/FR (structure — both `passages.json` and
  `useI18n.ts` dictionaries — supports adding more; not done yet)
- A backend endpoint returning each patient's latest assessment in one query;
  the dashboard currently fetches each patient's history in parallel
  client-side, fine at pilot-clinic scale but worth revisiting past a few
  hundred patients
- The clinical correlation study that would move this from "a well-engineered
  screening instrument" to "a validated one" — see the framing note at the top
  of this README
