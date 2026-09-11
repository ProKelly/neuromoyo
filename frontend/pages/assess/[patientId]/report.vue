<!--
  The synthesized cross-task report -- the whole point being that no single
  task's output IS the report. Backend (app/reporting.py) combines the
  reading-task risk trend with supporting measurements from the sustained-vowel
  and /pa-ta-ka/ tasks into one rule-based, fully-traceable recommendation; this
  page just renders that structure cleanly, plus a "Download as PDF" button
  that's just window.print() with print CSS -- no PDF library needed, the
  browser's own print-to-PDF does the work, and it stays pixel-identical to
  what's on screen.
-->
<template>
  <div>
    <div v-if="loading" class="text-ink-soft text-sm">Generating report…</div>
    <div v-else-if="error" class="bg-white border border-rust-100 rounded-2xl p-6 text-rust-600 text-sm">{{ error }}</div>

    <div v-else-if="report" id="report-root" class="bg-white border border-mist rounded-2xl p-6 sm:p-8 print:border-0 print:p-0">
      <!-- Report header -->
      <div class="flex flex-wrap items-start justify-between gap-4 mb-6 pb-6 border-b border-mist">
        <div>
          <Logo size="sm" :show-tagline="false" />
          <h1 class="font-display text-2xl font-medium text-ink mt-3">{{ t('report.title') }}</h1>
          <p class="text-sm text-ink-soft mt-1">
            {{ report.patient.display_id }}
            <span v-if="report.patient.age"> · {{ report.patient.age }}y</span>
            <span v-if="report.patient.sex"> · {{ report.patient.sex }}</span>
            <span v-if="report.patient.facility"> · {{ report.patient.facility }}</span>
          </p>
        </div>
        <div class="text-left sm:text-right text-xs text-ink-soft shrink-0">
          <p>{{ t('report.generatedOn') }}: {{ fmtDate(report.generated_at) }}</p>
          <p v-if="report.date_range_start && report.date_range_end" class="mt-0.5">
            {{ t('report.coverage') }}: {{ fmtDate(report.date_range_start) }} – {{ fmtDate(report.date_range_end) }}
          </p>
        </div>
      </div>

      <!-- Recommendation -->
      <div class="rounded-xl p-5 mb-6" :class="tierBg(report.recommendation_tier)">
        <p class="text-xs font-semibold uppercase tracking-wide mb-1.5" :class="tierText(report.recommendation_tier)">
          {{ t('report.recommendation') }} · {{ t(`report.tier.${report.recommendation_tier}`) }}
        </p>
        <p class="text-ink leading-relaxed">{{ report.recommendation_text }}</p>
      </div>

      <!-- Task completion -->
      <div class="mb-6">
        <h2 class="text-xs font-semibold text-ink-soft uppercase tracking-wide mb-3">{{ t('report.taskSummary') }}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div v-for="ts in report.task_summaries" :key="ts.task" class="border border-mist rounded-xl p-3.5">
            <p class="text-sm font-medium text-ink">{{ t(`report.task.${ts.task}`) }}</p>
            <p v-if="ts.count === 0" class="text-xs text-ink-soft mt-1">{{ t('report.notCompleted') }}</p>
            <template v-else>
              <p class="text-xs text-ink-soft mt-1">{{ ts.count }} {{ t('report.assessmentsCount') }}</p>
              <p v-if="ts.latest_risk_band" class="font-mono text-xs px-2 py-0.5 rounded-full inline-block mt-1.5" :class="bandBadgeClass(ts.latest_risk_band)">
                {{ Math.round((ts.latest_risk_score ?? 0) * 100) }}% · {{ ts.latest_risk_band }}
              </p>
            </template>
          </div>
        </div>
      </div>

      <!-- Reading risk trend -->
      <div v-if="readingPoints.length" class="mb-6">
        <h2 class="text-xs font-semibold text-ink-soft uppercase tracking-wide mb-2">
          {{ t('report.readingTrend') }}
          <span class="normal-case font-normal">({{ directionLabel(report.reading_trend_direction) }})</span>
        </h2>
        <TrendChart :points="readingPoints" />
      </div>

      <!-- Biomarker trends -->
      <div v-if="report.biomarker_trends.length" class="mb-6">
        <h2 class="text-xs font-semibold text-ink-soft uppercase tracking-wide mb-3">{{ t('report.biomarkerTrends') }}</h2>
        <div class="flex flex-col gap-5">
          <div v-for="bt in report.biomarker_trends" :key="bt.code">
            <p class="text-sm text-ink font-medium mb-1">
              {{ bt.label }} <span class="text-ink-soft font-normal">({{ directionLabel(bt.direction) }})</span>
            </p>
            <TrendChart :points="bt.points" color="var(--color-ink-soft)" />
          </div>
        </div>
      </div>

      <!-- Supporting findings -->
      <div class="mb-6">
        <h2 class="text-xs font-semibold text-ink-soft uppercase tracking-wide mb-2">{{ t('report.supportingFindings') }}</h2>
        <p v-if="report.supporting_findings.length === 0" class="text-sm text-ink-soft">{{ t('report.noFindings') }}</p>
        <ul v-else class="list-disc list-inside text-sm text-ink leading-relaxed flex flex-col gap-1.5">
          <li v-for="(f, i) in report.supporting_findings" :key="i">{{ f }}</li>
        </ul>
      </div>

      <p class="text-xs text-ink-soft pt-4 border-t border-mist">{{ report.disclaimer }}</p>
    </div>

    <button
      v-if="report"
      @click="downloadPdf"
      class="print:hidden mt-6 rounded-full bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold px-5 py-2.5 transition-colors cursor-pointer"
    >
      {{ t('report.download') }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { PatientReport } from '~/composables/useApi'

const patientId = inject<string>('patientId')!
const api = useApi()
const { t } = useI18n()

const report = ref<PatientReport | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    report.value = await api.getPatientReport(patientId)
  } catch (e: any) {
    error.value = e?.data?.detail || 'Could not generate the report.'
  } finally {
    loading.value = false
  }
})

const readingPoints = computed(() => report.value?.reading_points || [])

function fmtDate(d: string) {
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

function tierBg(tier: string) {
  if (tier === 'priority_referral') return 'bg-rust-100'
  if (tier === 'monitor') return 'bg-gold-100'
  if (tier === 'routine') return 'bg-teal-50'
  return 'bg-mist'
}
function tierText(tier: string) {
  if (tier === 'priority_referral') return 'text-rust-600'
  if (tier === 'monitor') return 'text-gold-600'
  if (tier === 'routine') return 'text-teal-600'
  return 'text-ink-soft'
}
function bandBadgeClass(band: string | null) {
  if (band === 'elevated') return 'bg-rust-100 text-rust-600'
  if (band === 'moderate') return 'bg-gold-100 text-gold-600'
  return 'bg-teal-50 text-teal-600'
}
function directionLabel(dir: string | null) {
  if (dir === 'increasing') return '↑ increasing'
  if (dir === 'decreasing') return '↓ decreasing'
  if (dir === 'stable') return '→ stable'
  return 'insufficient data'
}

function downloadPdf() {
  window.print()
}
</script>
