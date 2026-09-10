-- NEUROMOYO Voice Intelligence schema extension
-- Run against the production Supabase Postgres database once.
-- Safe to re-run. SQLModel create_all will create the base tables on a fresh DB,
-- but it does not alter existing tables, so this migration is required after v1.

CREATE TABLE IF NOT EXISTS voiceintelligencesession (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient(id),
    assessment_id UUID NULL REFERENCES assessment(id),
    language VARCHAR NULL,
    asr_provider VARCHAR NOT NULL,
    asr_model VARCHAR NOT NULL,
    transcript TEXT NOT NULL,
    asr_latency_ms DOUBLE PRECISION NULL,
    audio_duration_s DOUBLE PRECISION NULL,
    audio_quality_score DOUBLE PRECISION NULL,
    consent_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_voiceintelligencesession_patient_id
    ON voiceintelligencesession(patient_id);
CREATE INDEX IF NOT EXISTS ix_voiceintelligencesession_assessment_id
    ON voiceintelligencesession(assessment_id);

CREATE TABLE IF NOT EXISTS clinicalfinding (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES voiceintelligencesession(id),
    category VARCHAR NOT NULL,
    concept VARCHAR NOT NULL,
    value VARCHAR NULL,
    status VARCHAR NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    evidence TEXT NULL,
    source VARCHAR NOT NULL DEFAULT 'patient_speech'
);

CREATE INDEX IF NOT EXISTS ix_clinicalfinding_session_id
    ON clinicalfinding(session_id);
CREATE INDEX IF NOT EXISTS ix_clinicalfinding_category
    ON clinicalfinding(category);
CREATE INDEX IF NOT EXISTS ix_clinicalfinding_concept
    ON clinicalfinding(concept);

-- If the table was created by an earlier competition-ready build, add the
-- consent field without destroying existing sessions.
ALTER TABLE voiceintelligencesession
    ADD COLUMN IF NOT EXISTS consent_confirmed BOOLEAN NOT NULL DEFAULT FALSE;
