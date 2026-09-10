// Thin typed wrapper around the FastAPI backend. Centralizing calls here means
// backend contract changes surface in one file, not scattered across pages.
//
// Every call now attaches `Authorization: Bearer <token>` from the current
// Supabase session -- every backend route requires it (see backend/app/auth.py).
// `performer` is no longer sent by the client: the backend derives it from the
// authenticated clinician, since a logged-in identity is more trustworthy than
// whatever a client happened to send in a form field.

export interface Patient {
  id: string
  display_id: string
  age: number | null
  sex: string | null
  language: string | null
  facility: string | null
  existing_pd_diagnosis: boolean | null
  on_pd_medication: boolean | null
  created_at: string
}

export interface PatientCreate {
  display_id: string
  age?: number | null
  sex?: string | null
  language?: string | null
  facility?: string | null
  existing_pd_diagnosis?: boolean | null
  on_pd_medication?: boolean | null
}

export interface PatientUpdate {
  display_id?: string
  age?: number | null
  sex?: string | null
  language?: string | null
  facility?: string | null
  existing_pd_diagnosis?: boolean | null
  on_pd_medication?: boolean | null
}

export interface Biomarker {
  code: string
  label: string
  value: number
  shap_contribution: number | null
}

export interface ScreenResult {
  ok: boolean
  error?: string | null
  assessment_id?: string | null
  modality?: string | null
  task?: string | null
  risk_score?: number | null
  threshold?: number | null
  flagged?: boolean | null
  risk_band?: string | null
  confidence?: number | null
  quality_score?: number | null
  voiced_sec?: number | null
  n_windows?: number | null
  n_recordings?: number | null
  narrative?: string | null
  biomarkers: Biomarker[]
  disclaimer?: string | null
}

export interface ClinicalFinding {
  category: string
  concept: string
  value: string | null
  status: string
  confidence: number
  evidence: string | null
  source: string
}

export interface NeurologicalSignal {
  risk_score: number | null
  risk_band: string | null
  confidence: number | null
  quality_score: number | null
  biomarkers: Biomarker[]
  model_name: string | null
  model_version: string | null
}

export interface VoiceIntelligenceResult {
  ok: boolean
  error?: string | null
  session_id?: string | null
  assessment_id?: string | null
  transcript?: string | null
  language?: string | null
  asr_provider?: string | null
  asr_model?: string | null
  asr_latency_ms?: number | null
  audio_duration_s?: number | null
  audio_quality_score?: number | null
  consent_confirmed?: boolean
  clinical_findings: ClinicalFinding[]
  neurological_signal?: NeurologicalSignal | null
  clinician_summary?: string | null
  safety_notes: string[]
  created_at?: string | null
}

export interface Assessment {
  id: string
  patient_id: string
  modality: string
  task: string
  performer: string | null
  model_name: string | null
  model_version: string | null
  quality_score: number | null
  risk_score: number | null
  confidence: number | null
  risk_band: string | null
  flagged: boolean | null
  narrative: string | null
  voiced_sec: number | null
  n_windows: number | null
  n_recordings: number | null
  created_at: string
  biomarkers: Biomarker[]
}

export interface ClinicianMe {
  id: string
  email: string
  full_name: string | null
  role: string
  facility_id: string | null
  facility: string | null
  created_at: string
}

export interface Facility {
  id: string
  name: string
  created_at: string
}

export interface InviteClinicianPayload {
  email: string
  facility_id: string
  role: 'clinician' | 'facility_admin'
}

export interface TrendPoint {
  date: string
  value: number
}

export interface BiomarkerTrend {
  code: string
  label: string
  points: TrendPoint[]
  direction: 'increasing' | 'decreasing' | 'stable' | 'insufficient_data'
}

export interface TaskSummary {
  task: 'reading' | 'vowel' | 'ddk'
  count: number
  last_date: string | null
  latest_risk_score: number | null
  latest_risk_band: string | null
}

export interface PatientReport {
  patient: Patient
  generated_at: string
  date_range_start: string | null
  date_range_end: string | null
  total_assessments: number
  task_summaries: TaskSummary[]
  latest_reading: Assessment | null
  reading_points: TrendPoint[]
  reading_trend_direction: 'increasing' | 'decreasing' | 'stable' | 'insufficient_data' | null
  biomarker_trends: BiomarkerTrend[]
  recommendation_tier: 'priority_referral' | 'monitor' | 'routine' | 'insufficient_data'
  recommendation_text: string
  supporting_findings: string[]
  disclaimer: string
}

export function useApi() {
  const { public: { apiBase } } = useRuntimeConfig()
  const { getAccessToken } = useAuth()

  async function authHeaders(): Promise<Record<string, string>> {
    const token = await getAccessToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  async function createPatient(payload: PatientCreate): Promise<Patient> {
    return await $fetch<Patient>(`${apiBase}/api/patients`, {
      method: 'POST', body: payload, headers: await authHeaders(),
    })
  }

  async function listPatients(): Promise<Patient[]> {
    return await $fetch<Patient[]>(`${apiBase}/api/patients`, { headers: await authHeaders() })
  }

  async function getPatient(id: string): Promise<Patient> {
    return await $fetch<Patient>(`${apiBase}/api/patients/${id}`, { headers: await authHeaders() })
  }

  async function updatePatient(id: string, payload: PatientUpdate): Promise<Patient> {
    return await $fetch<Patient>(`${apiBase}/api/patients/${id}`, {
      method: 'PATCH', body: payload, headers: await authHeaders(),
    })
  }

  async function listFacilities(): Promise<Facility[]> {
    return await $fetch<Facility[]>(`${apiBase}/api/facilities`, { headers: await authHeaders() })
  }

  async function createFacility(name: string): Promise<Facility> {
    return await $fetch<Facility>(`${apiBase}/api/facilities`, {
      method: 'POST', body: { name }, headers: await authHeaders(),
    })
  }

  async function listClinicians(): Promise<ClinicianMe[]> {
    return await $fetch<ClinicianMe[]>(`${apiBase}/api/clinicians`, { headers: await authHeaders() })
  }

  async function inviteClinician(payload: InviteClinicianPayload): Promise<ClinicianMe> {
    return await $fetch<ClinicianMe>(`${apiBase}/api/clinicians/invite`, {
      method: 'POST', body: payload, headers: await authHeaders(),
    })
  }

  async function listPatientAssessments(id: string): Promise<Assessment[]> {
    return await $fetch<Assessment[]>(`${apiBase}/api/patients/${id}/assessments`, { headers: await authHeaders() })
  }

  async function getMe(): Promise<ClinicianMe> {
    return await $fetch<ClinicianMe>(`${apiBase}/api/clinicians/me`, { headers: await authHeaders() })
  }

  async function getPatientReport(id: string): Promise<PatientReport> {
    return await $fetch<PatientReport>(`${apiBase}/api/patients/${id}/report`, { headers: await authHeaders() })
  }

  async function analyseVoiceIntelligence(patientId: string, blob: Blob, language = 'en', consentConfirmed = false): Promise<VoiceIntelligenceResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    form.append('language', language)
    form.append('consent_confirmed', String(consentConfirmed))
    form.append('audio', blob, 'voice-intelligence.webm')
    return await $fetch<VoiceIntelligenceResult>(`${apiBase}/api/voice-intelligence/analyse`, {
      method: 'POST', body: form, headers: await authHeaders(),
    })
  }

  async function screenReading(patientId: string, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    form.append('audio', blob, 'reading.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/reading`, {
      method: 'POST', body: form, headers: await authHeaders(),
    })
  }

  async function screenVowel(patientId: string, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    form.append('audio', blob, 'vowel.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/vowel`, {
      method: 'POST', body: form, headers: await authHeaders(),
    })
  }

  async function screenDdk(patientId: string, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    form.append('audio', blob, 'ddk.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/ddk`, {
      method: 'POST', body: form, headers: await authHeaders(),
    })
  }

  return { createPatient, listPatients, getPatient, updatePatient, listFacilities, createFacility, listClinicians, inviteClinician, listPatientAssessments, getMe, getPatientReport, analyseVoiceIntelligence, screenReading, screenVowel, screenDdk }
}
