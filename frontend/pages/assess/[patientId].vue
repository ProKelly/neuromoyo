<template>
  <div v-if="patient">
    <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2">Step 2 of 2</p>
    <h1 class="font-display text-3xl font-medium text-ink mb-1">{{ patient.display_id }}</h1>
    <p class="text-ink-soft mb-6">
      {{ patient.facility || 'No facility on file' }} · {{ (patient.language || 'en').toUpperCase() }}
    </p>

    <nav class="flex gap-2 mb-6 flex-wrap">
      <button
        v-for="t in tabs" :key="t.id"
        class="rounded-full px-4 py-2 text-sm font-medium border transition-colors cursor-pointer"
        :class="tab === t.id
          ? 'bg-teal-600 text-white border-teal-600'
          : 'bg-white text-ink-soft border-mist hover:border-teal-600/50'"
        @click="onTab(t.id)"
      >
        {{ t.label }}
      </button>
    </nav>

    <section v-if="tab === 'reading'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Reading passage</h2>
      <p class="text-sm text-ink-soft mb-4">Read the passage aloud, clearly, for about 30 seconds.</p>
      <p class="leading-relaxed text-ink bg-paper rounded-xl p-4 mb-5 border border-mist">{{ passageText }}</p>
      <Recorder @recorded="(b) => submit('reading', b)" />
    </section>

    <section v-if="tab === 'vowel'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Sustained vowel</h2>
      <p class="text-sm text-ink-soft mb-5">Take a breath and hold a steady "aaah" for 5–10 seconds.</p>
      <Recorder @recorded="(b) => submit('vowel', b)" />
    </section>

    <section v-if="tab === 'ddk'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Diadochokinetic (/pa-ta-ka/)</h2>
      <p class="text-sm text-ink-soft mb-5">Repeat "pa-ta-ka" as fast and evenly as possible for about 5 seconds.</p>
      <Recorder @recorded="(b) => submit('ddk', b)" />
    </section>

    <section v-if="tab === 'history'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Assessment history</h2>
      <p v-if="history.length === 0" class="text-sm text-ink-soft mt-2">No assessments recorded yet.</p>
      <ul v-else class="mt-3 divide-y divide-mist">
        <li v-for="a in history" :key="a.id" class="py-3 flex items-center justify-between text-sm">
          <div>
            <span class="font-medium text-ink capitalize">{{ a.task }}</span>
            <span class="text-ink-soft ml-2">{{ new Date(a.created_at).toLocaleString() }}</span>
          </div>
          <span v-if="a.risk_score !== null" class="font-mono text-xs px-2 py-1 rounded-full" :class="bandBadgeClass(a.risk_band)">
            {{ Math.round((a.risk_score ?? 0) * 100) }}% · {{ a.risk_band }}
          </span>
        </li>
      </ul>
    </section>

    <div v-if="submitting" class="flex items-center gap-2 text-sm text-ink-soft mb-6">
      <span class="w-2 h-2 rounded-full bg-teal-600 animate-pulse"></span>
      Analyzing…
    </div>

    <div v-if="result" class="bg-white border border-mist rounded-2xl p-6">
      <p v-if="!result.ok" class="text-sm text-rust-600">{{ result.error }}</p>
      <template v-else>
        <div v-if="result.risk_score !== null && result.risk_score !== undefined" class="flex flex-col items-center mb-4">
          <RiskGauge :score="result.risk_score" :band="result.risk_band || 'low'" />
        </div>
        <p class="text-ink leading-relaxed">{{ result.narrative }}</p>

        <table v-if="result.biomarkers.length" class="w-full mt-5 text-sm">
          <tbody>
            <tr v-for="b in result.biomarkers" :key="b.code" class="border-t border-mist first:border-t-0">
              <td class="py-2 text-ink-soft">{{ b.label }}</td>
              <td class="py-2 text-right font-mono text-ink">{{ b.value }}</td>
            </tr>
          </tbody>
        </table>

        <p v-if="result.disclaimer" class="text-xs text-ink-soft mt-5 pt-4 border-t border-mist">
          {{ result.disclaimer }}
        </p>
      </template>
    </div>
  </div>
  <div v-else class="text-ink-soft">Loading patient…</div>
</template>

<script setup lang="ts">
import type { Assessment, Patient, ScreenResult } from '~/composables/useApi'
import passages from '~/assets/passages.json'

const route = useRoute()
const api = useApi()
const patientId = route.params.patientId as string

const tabs = [
  { id: 'reading', label: 'Reading' },
  { id: 'vowel', label: 'Sustained vowel' },
  { id: 'ddk', label: '/pa-ta-ka/' },
  { id: 'history', label: 'History' },
] as const

const patient = ref<Patient | null>(null)
const tab = ref<typeof tabs[number]['id']>('reading')
const submitting = ref(false)
const result = ref<ScreenResult | null>(null)
const history = ref<Assessment[]>([])

const passageText = computed(() => {
  const lang = patient.value?.language || 'en'
  return (passages as Record<string, { text: string }>)[lang]?.text
    || (passages as Record<string, { text: string }>).en.text
})

onMounted(async () => {
  patient.value = await api.getPatient(patientId)
})

async function onTab(id: typeof tabs[number]['id']) {
  tab.value = id
  result.value = null
  if (id === 'history') history.value = await api.listPatientAssessments(patientId)
}

function bandBadgeClass(band: string | null) {
  if (band === 'elevated') return 'bg-rust-100 text-rust-600'
  if (band === 'moderate') return 'bg-gold-100 text-gold-600'
  return 'bg-teal-50 text-teal-600'
}

async function submit(task: 'reading' | 'vowel' | 'ddk', blob: Blob) {
  submitting.value = true
  result.value = null
  try {
    if (task === 'reading') result.value = await api.screenReading(patientId, undefined, blob)
    if (task === 'vowel') result.value = await api.screenVowel(patientId, undefined, blob)
    if (task === 'ddk') result.value = await api.screenDdk(patientId, undefined, blob)
  } catch (e) {
    result.value = { ok: false, error: 'Analysis failed. Check the backend connection and try again.', biomarkers: [] }
  } finally {
    submitting.value = false
  }
}
</script>
