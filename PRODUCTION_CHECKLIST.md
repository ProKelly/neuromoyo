# NEUROMOYO Competition Production Checklist

## Before enabling Voice Intelligence

- [ ] Rotate any credentials that were included in local archives.
- [ ] Set `VOICE_INTELLIGENCE_ENABLED=true` only in the backend deployment environment.
- [ ] Set `SAHARA_API_KEY` only as a backend secret.
- [ ] Set `CORS_ORIGINS` to the exact production frontend origin(s), never `*`.
- [ ] Set `FRONTEND_URL` to the deployed frontend URL.
- [ ] Run `backend/migrations/001_voice_intelligence.sql` against the production database.
- [ ] Confirm Supabase RLS/access policies appropriate to the project's deployment model.
- [ ] Verify `/api/health` and `/api/ready`.
- [ ] Test clinician authentication and facility scoping.
- [ ] Test consent-required recording flow.
- [ ] Test 20–60 second natural speech in a supported browser.
- [ ] Confirm temporary audio files are deleted after processing.
- [ ] Confirm transcript/finding persistence in the patient's history.
- [ ] Confirm provider/API errors return generic client messages with request IDs.

## Competition evidence

- Benchmark evidence is separate from the production runtime.
- The AfriSwitch Pidgin benchmark remains reproducible from the clean Colab notebook.
- Do not claim a CS/non-CS penalty from the Pidgin split: it contains only two non-code-switched examples.
- Report CMI, switch-point and duration robustness instead.
- Do not publish raw patient/health-related audio without explicit consent and a suitable data-sharing basis.
