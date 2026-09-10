# Competition Build Changelog

## v2 — production hardening

- Isolated Voice Intelligence module and router.
- Added Sahara ASR abstraction and provider adapter.
- Canonicalised uploaded audio to 16 kHz mono WAV before downstream processing.
- Added audio duration, speech, clipping and size validation.
- Added explicit patient consent confirmation at UI and API boundaries.
- Added traceable clinical findings with evidence snippets.
- Persisted ASR/model provenance and consent status.
- Added request IDs and generic external error messages.
- Added exact production CORS enforcement and optional database auto-creation.
- Added production SQL migration for Voice Intelligence tables.
- Added paginated Voice Intelligence history.
- Added public `/benchmark` evidence page backed by static frozen results.
- Added competition benchmark evidence package under `research/hackathon/`.
- Corrected benchmark documentation so it does not claim a CS/non-CS penalty that cannot be estimated from the AfriSwitch Pidgin split.
- Removed “research prototype” wording from the clinician-facing screening disclaimer.
