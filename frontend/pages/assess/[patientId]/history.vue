<template>
  <div>
    <nav class="flex gap-2 mb-5">
      <button
        v-for="v in views" :key="v.id"
        class="rounded-full px-4 py-2 text-sm font-medium border transition-colors cursor-pointer"
        :class="view === v.id
          ? 'bg-teal-600 text-white border-teal-600'
          : 'bg-white text-ink-soft border-mist hover:border-teal-600/50'"
        @click="view = v.id"
      >
        {{ t(v.labelKey) }}
      </button>
    </nav>

    <section v-if="view === 'list'" class="bg-white border border-mist rounded-2xl p-6">
      <p v-if="loading" class="text-sm text-ink-soft">Loading…</p>
      <p v-else-if="history.length === 0" class="text-sm text-ink-soft">No assessments recorded yet.</p>
      <ul v-else class="divide-y divide-mist">
        <li v-for="a in history" :key="a.id" class="py-3 flex items-center justify-between text-sm">
          <div>
            <span class="font-medium text-ink capitalize">{{ a.task }}</span>
            <span class="text-ink-soft ml-2">{{ new Date(a.created_at).toLocaleString() }}</span>
            <span v-if="a.performer" class="text-ink-soft ml-2">· {{ a.performer }}</span>
          </div>
          <span v-if="a.risk_score !== null" class="font-mono text-xs px-2 py-1 rounded-full" :class="bandBadgeClass(a.risk_band)">
            {{ Math.round((a.risk_score ?? 0) * 100) }}% · {{ a.risk_band }}
          </span>
        </li>
      </ul>
    </section>

    <section v-if="view === 'trends'" class="bg-white border border-mist rounded-2xl p-6">
      <p class="text-sm text-ink-soft mb-5">
        How this patient's measurements have moved across assessments — the point of NeuroMonitor
        is change over time, not any single reading.
      </p>

      <p v-if="loading" class="text-sm text-ink-soft">Loading…</p>

      <template v-else>
        <div v-if="riskSeries.length" class="mb-8">
          <h3 class="text-xs font-semibold text-ink-soft uppercase tracking-wide mb-2">Risk score · reading task</h3>
          <TrendChart :points="riskSeries" />
        </div>

        <div v-if="biomarkerOptions.length">
          <div class="flex items-center justify-between mb-2 flex-wrap gap-2">
            <h3 class="text-xs font-semibold text-ink-soft uppercase tracking-wide">Biomarker</h3>
            <select
              v-model="trendBiomarker"
              class="rounded-lg border border-mist px-3 py-1.5 text-sm text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600"
            >
              <option v-for="o in biomarkerOptions" :key="o.code" :value="o.code">
                {{ o.label }} ({{ o.count }})
              </option>
            </select>
          </div>
          <TrendChart :points="biomarkerSeries" color="var(--color-ink-soft)" />
          <p v-if="trendNote" class="text-sm text-ink leading-relaxed mt-3">{{ trendNote }}</p>
        </div>

        <p v-if="!riskSeries.length && !biomarkerOptions.length" class="text-sm text-ink-soft">
          Not enough repeat assessments yet — trends need at least two assessments with the same
          measurement to show change over time.
        </p>
      </template>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { Assessment } from '~/composables/useApi'

const patientId = inject<string>('patientId')!
const api = useApi()
const { t } = useI18n()

const views = [
  { id: 'list', labelKey: 'assess.tab.history' },
  { id: 'trends', labelKey: 'assess.tab.trends' },
] as const

const view = ref<typeof views[number]['id']>('list')
const history = ref<Assessment[]>([])
const loading = ref(true)
const trendBiomarker = ref<string | null>(null)

onMounted(async () => {
  try {
    history.value = await api.listPatientAssessments(patientId)
  } finally {
    loading.value = false
  }
})

function bandBadgeClass(band: string | null) {
  if (band === 'elevated') return 'bg-rust-100 text-rust-600'
  if (band === 'moderate') return 'bg-gold-100 text-gold-600'
  return 'bg-teal-50 text-teal-600'
}

const riskSeries = computed(() =>
  history.value
    .filter((a) => a.risk_score !== null && a.risk_score !== undefined)
    .map((a) => ({ date: a.created_at, value: a.risk_score as number, band: a.risk_band }))
)

interface BiomarkerOption { code: string; label: string; count: number }

const biomarkerOptions = computed<BiomarkerOption[]>(() => {
  const seen = new Map<string, BiomarkerOption>()
  for (const a of history.value) {
    for (const b of a.biomarkers) {
      const entry = seen.get(b.code)
      if (entry) entry.count++
      else seen.set(b.code, { code: b.code, label: b.label, count: 1 })
    }
  }
  return [...seen.values()]
    .filter((o) => o.count >= 2)
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label))
})

watch(biomarkerOptions, (opts) => {
  if (!opts.length) { trendBiomarker.value = null; return }
  if (!trendBiomarker.value || !opts.some((o) => o.code === trendBiomarker.value)) {
    trendBiomarker.value = opts[0].code
  }
})

const biomarkerSeries = computed(() => {
  if (!trendBiomarker.value) return []
  return history.value
    .filter((a) => a.biomarkers.some((b) => b.code === trendBiomarker.value))
    .map((a) => ({
      date: a.created_at,
      value: a.biomarkers.find((b) => b.code === trendBiomarker.value)!.value,
    }))
})

const selectedBiomarkerLabel = computed(() => {
  const opt = biomarkerOptions.value.find((o) => o.code === trendBiomarker.value)
  return opt?.label || trendBiomarker.value || 'This measurement'
})

const trendNote = computed(() => {
  const series = biomarkerSeries.value
  if (series.length < 2) return null
  const first = series[0].value
  const last = series[series.length - 1].value
  const delta = last - first
  const days = Math.round(
    (new Date(series[series.length - 1].date).getTime() - new Date(series[0].date).getTime()) / 86_400_000
  )
  const span = days >= 14 ? `${Math.round(days / 7)} weeks` : `${Math.max(days, 1)} day${days === 1 ? '' : 's'}`
  if (Math.abs(delta) < Math.abs(first || 1) * 0.02) {
    return `${selectedBiomarkerLabel.value} has stayed roughly steady across ${series.length} assessments over ${span}.`
  }
  const dir = delta > 0 ? 'increased' : 'decreased'
  return `${selectedBiomarkerLabel.value} has ${dir} over the last ${span}, across ${series.length} assessments.`
})
</script>
