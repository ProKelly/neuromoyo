<!--
  Clinician dashboard: the patient roster for the signed-in clinician's facility
  (or every facility, for an admin -- see backend/app/routers/patients.py), with
  each patient's most recent screening result and risk trend so a clinician can
  scan "who needs a closer look" at a glance rather than opening patients one by
  one. This is the NeuroMonitor view from the engineering blueprint's Phase 4,
  built directly on the same Assessment history endpoint the per-patient page uses.
-->
<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="font-display text-3xl font-medium text-ink mb-1">{{ t('dashboard.title') }}</h1>
        <p class="text-ink-soft">{{ t('dashboard.subtitle') }}</p>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <LanguageToggle />
        <NuxtLink
          to="/patients/new"
          class="rounded-full bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold px-4 py-2.5 transition-colors whitespace-nowrap"
        >
          + {{ t('dashboard.addPatient') }}
        </NuxtLink>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-2 sm:gap-3 mb-6">
      <div class="bg-white border border-mist rounded-xl p-3 sm:p-4">
        <p class="text-xl sm:text-2xl font-display font-medium text-ink">{{ patients.length }}</p>
        <p class="text-[11px] sm:text-xs text-ink-soft mt-0.5">{{ t('dashboard.stat.total') }}</p>
      </div>
      <div class="bg-white border border-mist rounded-xl p-3 sm:p-4">
        <p class="text-xl sm:text-2xl font-display font-medium" :class="flaggedCount > 0 ? 'text-rust-600' : 'text-ink'">{{ flaggedCount }}</p>
        <p class="text-[11px] sm:text-xs text-ink-soft mt-0.5">{{ t('dashboard.stat.flagged') }}</p>
      </div>
      <div class="bg-white border border-mist rounded-xl p-3 sm:p-4">
        <p class="text-xl sm:text-2xl font-display font-medium text-ink">{{ assessmentsThisMonth }}</p>
        <p class="text-[11px] sm:text-xs text-ink-soft mt-0.5">{{ t('dashboard.stat.assessments') }}</p>
      </div>
    </div>

    <div class="flex flex-col sm:flex-row gap-3 mb-4">
      <input
        v-model="search" type="search" :placeholder="t('dashboard.search')"
        class="flex-1 rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 bg-white focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
      />
      <div class="flex gap-2">
        <button
          v-for="f in filters" :key="f.id"
          class="rounded-full px-4 py-2 text-sm font-medium border transition-colors cursor-pointer whitespace-nowrap"
          :class="filter === f.id ? 'bg-teal-600 text-white border-teal-600' : 'bg-white text-ink-soft border-mist hover:border-teal-600/50'"
          @click="filter = f.id"
        >
          {{ t(f.labelKey) }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-ink-soft text-sm">Loading…</div>

    <div v-else-if="filteredRows.length === 0" class="bg-white border border-mist rounded-2xl p-8 text-center text-ink-soft text-sm">
      {{ filter === 'flagged' && !search
        ? `No patients are currently flagged — ${flaggedCount} of ${patients.length} need review right now.`
        : (search || filter !== 'all' ? t('dashboard.empty.filtered') : t('dashboard.empty')) }}
    </div>

    <div v-else class="flex flex-col gap-3">
      <NuxtLink
        v-for="row in filteredRows" :key="row.patient.id" :to="`/assess/${row.patient.id}`"
        class="bg-white border border-mist rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center gap-4 hover:border-teal-600/50 transition-colors"
      >
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-semibold text-ink">{{ row.patient.display_id }}</span>
            <span
              v-if="row.latest?.risk_band"
              class="font-mono text-xs px-2 py-0.5 rounded-full"
              :class="bandBadgeClass(row.latest.risk_band)"
            >
              {{ Math.round((row.latest.risk_score ?? 0) * 100) }}% · {{ row.latest.risk_band }}
            </span>
          </div>
          <p class="text-sm text-ink-soft mt-0.5 truncate">
            {{ row.patient.facility || '—' }}
            <span v-if="row.patient.age"> · {{ row.patient.age }}y</span>
          </p>
          <p class="text-xs text-ink-soft mt-1">
            {{ row.latest ? `${t('dashboard.col.lastAssessed')}: ${fmtDate(row.latest.created_at)}` : t('dashboard.noAssessments') }}
          </p>
        </div>

        <div v-if="row.trendPoints.length >= 2" class="w-full sm:w-40 shrink-0">
          <TrendChart :points="row.trendPoints" />
        </div>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Assessment, Patient } from '~/composables/useApi'

const api = useApi()
const { t } = useI18n()

const patients = ref<Patient[]>([])
const assessmentsByPatient = ref<Record<string, Assessment[]>>({})
const loading = ref(true)
const search = ref('')
const filter = ref<'all' | 'flagged'>('all')

const filters = [
  { id: 'all' as const, labelKey: 'dashboard.filter.all' },
  { id: 'flagged' as const, labelKey: 'dashboard.filter.flagged' },
]

onMounted(async () => {
  loading.value = true
  try {
    patients.value = await api.listPatients()
    // Per-patient history fetched in parallel. Fine at pilot-clinic scale (dozens
    // to low hundreds of patients); if a facility's roster grows much past that,
    // this is the natural point to add a backend endpoint that returns each
    // patient's latest assessment in one query instead of N round trips.
    const entries = await Promise.all(
      patients.value.map(async (p) => [p.id, await api.listPatientAssessments(p.id)] as const)
    )
    assessmentsByPatient.value = Object.fromEntries(entries)
  } finally {
    loading.value = false
  }
})

const rows = computed(() =>
  patients.value.map((patient) => {
    const history = assessmentsByPatient.value[patient.id] || []
    const scored = history.filter((a) => a.risk_score !== null)
    const latest = scored[scored.length - 1] || history[history.length - 1] || null
    const trendPoints = scored.map((a) => ({ date: a.created_at, value: a.risk_score as number, band: a.risk_band }))
    return { patient, latest, trendPoints }
  })
)

const flaggedCount = computed(() => rows.value.filter((r) => r.latest?.flagged).length)

const assessmentsThisMonth = computed(() => {
  const now = new Date()
  return Object.values(assessmentsByPatient.value).flat().filter((a) => {
    const d = new Date(a.created_at)
    return d.getFullYear() === now.getFullYear() && d.getMonth() === now.getMonth()
  }).length
})

const filteredRows = computed(() => {
  let out = rows.value
  if (filter.value === 'flagged') out = out.filter((r) => r.latest?.flagged)
  if (search.value.trim()) {
    const q = search.value.trim().toLowerCase()
    out = out.filter((r) => r.patient.display_id.toLowerCase().includes(q))
  }
  return out
})

function bandBadgeClass(band: string | null) {
  if (band === 'elevated') return 'bg-rust-100 text-rust-600'
  if (band === 'moderate') return 'bg-gold-100 text-gold-600'
  return 'bg-teal-50 text-teal-600'
}

function fmtDate(d: string) {
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>
