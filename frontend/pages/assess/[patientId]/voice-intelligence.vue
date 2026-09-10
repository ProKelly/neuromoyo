<template>
  <div class="space-y-6">
    <section class="bg-white border border-mist rounded-2xl p-6 md:p-8">
      <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-5">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-teal-600 mb-2">Voice Intelligence</p>
          <h2 class="font-display text-3xl font-medium text-ink">Natural speech → clinical evidence</h2>
          <p class="text-ink-soft mt-2 max-w-2xl">
            Capture natural patient speech, preserve African code-switched language, and turn the recording into
            traceable clinical information alongside Neuromoyo's existing neurological voice screen.
          </p>
        </div>
        <div class="rounded-xl bg-teal-50 border border-teal-100 px-4 py-3 text-sm text-teal-900">
          <div class="font-semibold">Clinician decision support</div>
          <div class="mt-1 text-teal-700">Not an autonomous diagnosis.</div>
        </div>
      </div>
    </section>

    <section class="bg-white border border-mist rounded-2xl p-6">
      <div class="grid md:grid-cols-3 gap-4 mb-6">
        <label class="block">
          <span class="text-sm font-medium text-ink">Patient speech language</span>
          <select v-model="language" class="mt-2 w-full rounded-xl border border-mist bg-white px-4 py-3 text-sm outline-none focus:border-teal-600">
            <option value="en">English / Pidgin + English</option>
            <option value="fr">French</option>
          </select>
        </label>
        <div class="rounded-xl bg-paper border border-mist px-4 py-3">
          <div class="text-xs uppercase tracking-wide text-ink-soft">Recording</div>
          <div class="font-medium text-ink mt-1">Natural conversation</div>
          <div class="text-xs text-ink-soft mt-1">Recommended 20–60 seconds</div>
        </div>
        <div class="rounded-xl bg-paper border border-mist px-4 py-3">
          <div class="text-xs uppercase tracking-wide text-ink-soft">Processing</div>
          <div class="font-medium text-ink mt-1">African speech recognition</div>
          <div class="text-xs text-ink-soft mt-1">Transcript + clinical extraction + voice signal</div>
        </div>
      </div>

      <div v-if="!result" class="max-w-xl mx-auto text-center py-6">
        <div class="mx-auto mb-5 w-20 h-20 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-700 text-3xl">◉</div>
        <h3 class="font-display text-2xl font-medium text-ink">Record the patient's natural speech</h3>
        <p class="text-sm text-ink-soft mt-2 mb-5">
          Ask the patient to describe their symptoms or day-to-day experience in their own words.
          They may speak naturally in English, Pidgin, or code-switch between them.
        </p>

        <label class="flex items-start gap-3 rounded-xl border border-mist bg-paper p-4 text-left mb-5 cursor-pointer">
          <input v-model="consentConfirmed" type="checkbox" class="mt-1 h-4 w-4 accent-teal-600" />
          <span class="text-sm text-ink-soft">
            I confirm that the patient has been informed that their speech will be analysed for clinical decision support and has consented to this recording and analysis.
          </span>
        </label>

        <Recorder :disabled="!consentConfirmed" @recorded="submit" />
      </div>

      <div v-if="submitting" class="py-10 text-center">
        <div class="mx-auto w-10 h-10 rounded-full border-2 border-teal-100 border-t-teal-600 animate-spin"></div>
        <h3 class="font-medium text-ink mt-4">Analysing speech</h3>
        <p class="text-sm text-ink-soft mt-1">Checking audio quality → transcribing → extracting clinical evidence → analysing voice.</p>
      </div>

      <div v-if="error" class="rounded-xl border border-rust-100 bg-rust-100/40 text-rust-700 p-4 text-sm">
        {{ error }}
      </div>
    </section>

    <section v-if="result?.ok" class="space-y-6">
      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white border border-mist rounded-2xl p-6">
          <div class="flex items-center justify-between gap-4 mb-4">
            <div>
              <h3 class="font-display text-xl font-medium text-ink">Clinical information extracted</h3>
              <p class="text-xs text-ink-soft mt-1">Evidence comes from the patient's recorded speech.</p>
            </div>
            <span class="rounded-full bg-teal-50 text-teal-700 px-3 py-1 text-xs font-medium">Traceable</span>
          </div>
          <div v-if="result.clinical_findings.length" class="grid md:grid-cols-2 gap-3">
            <article v-for="f in result.clinical_findings" :key="`${f.category}-${f.concept}-${f.status}`" class="rounded-xl border border-mist p-4">
              <div class="flex justify-between gap-3">
                <div>
                  <div class="text-xs uppercase tracking-wide text-ink-soft">{{ prettyCategory(f.category) }}</div>
                  <div class="font-medium text-ink mt-1 capitalize">{{ f.concept }}</div>
                </div>
                <div class="text-xs font-mono text-teal-700">{{ Math.round(f.confidence * 100) }}%</div>
              </div>
              <div class="text-sm mt-3" :class="f.status === 'absent' ? 'text-ink-soft' : 'text-ink'">{{ prettyStatus(f.status) }}</div>
              <div v-if="f.evidence" class="mt-3 rounded-lg bg-paper px-3 py-2 text-xs text-ink-soft">“{{ f.evidence }}”</div>
            </article>
          </div>
          <p v-else class="text-sm text-ink-soft">No predefined clinical finding was confidently extracted from this recording.</p>
        </div>

        <div class="bg-white border border-mist rounded-2xl p-6">
          <h3 class="font-display text-xl font-medium text-ink">Neurological voice signal</h3>
          <p class="text-xs text-ink-soft mt-1">Independent acoustic screening evidence.</p>
          <div v-if="result.neurological_signal" class="mt-5">
            <div class="text-xs uppercase tracking-wide text-ink-soft">Screening band</div>
            <div class="text-2xl font-semibold capitalize mt-1 text-ink">{{ result.neurological_signal.risk_band || 'Unavailable' }}</div>
            <div v-if="result.neurological_signal.risk_score !== null" class="mt-4">
              <RiskGauge :score="result.neurological_signal.risk_score || 0" :band="result.neurological_signal.risk_band || 'low'" />
            </div>
            <div class="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div class="rounded-lg bg-paper p-3"><div class="text-xs text-ink-soft">Confidence</div><div class="font-mono mt-1">{{ percent(result.neurological_signal.confidence) }}</div></div>
              <div class="rounded-lg bg-paper p-3"><div class="text-xs text-ink-soft">Quality</div><div class="font-mono mt-1">{{ percent(result.neurological_signal.quality_score) }}</div></div>
            </div>
          </div>
          <div v-else class="mt-5 rounded-xl bg-paper p-4 text-sm text-ink-soft">The neurological acoustic screen could not produce a usable result from this recording.</div>
        </div>
      </div>

      <div class="bg-white border border-mist rounded-2xl p-6">
        <div class="flex items-center justify-between gap-4 mb-4">
          <div>
            <h3 class="font-display text-xl font-medium text-ink">Transcript</h3>
            <p class="text-xs text-ink-soft mt-1">{{ result.asr_provider }} · {{ result.asr_model }} · {{ Math.round(result.asr_latency_ms || 0) }} ms</p>
          </div>
          <div class="text-xs rounded-full bg-paper border border-mist px-3 py-1">{{ result.language?.toUpperCase() }}</div>
        </div>
        <p class="leading-7 text-ink bg-paper rounded-xl p-5 whitespace-pre-wrap">{{ result.transcript }}</p>
      </div>

      <div class="bg-white border border-mist rounded-2xl p-6">
        <h3 class="font-display text-xl font-medium text-ink">Clinician summary</h3>
        <p class="mt-3 text-ink leading-7">{{ result.clinician_summary }}</p>
        <div class="mt-5 rounded-xl bg-teal-50 border border-teal-100 p-4">
          <div class="font-medium text-teal-900">Clinical interpretation</div>
          <p class="text-sm text-teal-800 mt-1">The extracted findings and voice signal are decision-support evidence. Verify them against the patient's history and examination before making a clinical decision.</p>
        </div>
      </div>

      <div class="bg-white border border-mist rounded-2xl p-6">
        <h3 class="font-display text-xl font-medium text-ink">Safety & provenance</h3>
        <ul class="mt-3 space-y-2 text-sm text-ink-soft list-disc pl-5">
          <li v-for="note in result.safety_notes" :key="note">{{ note }}</li>
        </ul>
        <div class="mt-5 pt-4 border-t border-mist flex flex-wrap gap-4 text-xs text-ink-soft">
          <span>Audio: temporary processing only</span>
          <span>Session: {{ result.session_id }}</span>
          <span>Duration: {{ (result.audio_duration_s || 0).toFixed(1) }}s</span>
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="rounded-xl bg-teal-600 text-white px-5 py-3 text-sm font-medium hover:bg-teal-700" @click="reset">New voice assessment</button>
        <NuxtLink :to="`/assess/${patientId}/history`" class="rounded-xl border border-mist bg-white px-5 py-3 text-sm font-medium text-ink-soft hover:border-teal-600/50">View patient history</NuxtLink>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { Patient, VoiceIntelligenceResult } from '~/composables/useApi'

const patientId = inject<string>('patientId')!
const patient = inject<Ref<Patient | null>>('patient')!
const api = useApi()

const language = ref(normaliseLanguage(patient.value?.language))
const submitting = ref(false)
const consentConfirmed = ref(false)
const result = ref<VoiceIntelligenceResult | null>(null)
const error = ref<string | null>(null)

watch(patient, (value) => {
  if (value?.language) language.value = normaliseLanguage(value.language)
})

async function submit(blob: Blob) {
  submitting.value = true
  result.value = null
  error.value = null
  try {
    result.value = await api.analyseVoiceIntelligence(patientId, blob, language.value, consentConfirmed.value)
    if (!result.value.ok) error.value = result.value.error || 'The recording could not be analysed.'
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || 'Voice Intelligence analysis failed. Please try again.'
  } finally {
    submitting.value = false
  }
}

function reset() {
  result.value = null
  error.value = null
}

function prettyCategory(value: string) {
  return value.replaceAll('_', ' ')
}
function prettyStatus(value: string) {
  return value === 'present' ? 'Present in speech' : value === 'absent' ? 'Negated in speech' : value.replaceAll('_', ' ')
}
function normaliseLanguage(value: string | null | undefined) {
  const v = (value || 'en').toLowerCase()
  return v === 'fr' || v.startsWith('fr') ? 'fr' : 'en'
}

function percent(value: number | null | undefined) {
  return value == null ? '—' : `${Math.round(value * 100)}%`
}
</script>
