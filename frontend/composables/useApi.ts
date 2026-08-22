// Thin typed wrapper around the FastAPI backend. Centralizing calls here means
// backend contract changes surface in one file, not scattered across pages.

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

export function useApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  async function createPatient(payload: PatientCreate): Promise<Patient> {
    return await $fetch<Patient>(`${apiBase}/api/patients`, { method: 'POST', body: payload })
  }

  async function getPatient(id: string): Promise<Patient> {
    return await $fetch<Patient>(`${apiBase}/api/patients/${id}`)
  }

  async function listPatientAssessments(id: string): Promise<Assessment[]> {
    return await $fetch<Assessment[]>(`${apiBase}/api/patients/${id}/assessments`)
  }

  async function screenReading(patientId: string, performer: string | undefined, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    if (performer) form.append('performer', performer)
    form.append('audio', blob, 'reading.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/reading`, { method: 'POST', body: form })
  }

  async function screenVowel(patientId: string, performer: string | undefined, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    if (performer) form.append('performer', performer)
    form.append('audio', blob, 'vowel.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/vowel`, { method: 'POST', body: form })
  }

  async function screenDdk(patientId: string, performer: string | undefined, blob: Blob): Promise<ScreenResult> {
    const form = new FormData()
    form.append('patient_id', patientId)
    if (performer) form.append('performer', performer)
    form.append('audio', blob, 'ddk.webm')
    return await $fetch<ScreenResult>(`${apiBase}/api/assessments/voice/ddk`, { method: 'POST', body: form })
  }

  return { createPatient, getPatient, listPatientAssessments, screenReading, screenVowel, screenDdk }
}
