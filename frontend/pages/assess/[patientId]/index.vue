<template>
  <div>
    <div class="bg-white border border-mist rounded-2xl p-5 sm:p-6 mb-6">
      <h2 class="text-xs font-semibold tracking-wide uppercase text-ink-soft mb-3">{{ t('overview.status') }}</h2>
      <div v-if="loading" class="text-sm text-ink-soft">Loading…</div>
      <div v-else-if="!latestReading" class="text-sm text-ink-soft">{{ t('overview.notScreened') }}</div>
      <div v-else class="flex items-center gap-4 flex-wrap">
        <span
          class="font-mono text-sm px-3 py-1.5 rounded-full font-semibold"
          :class="bandBadgeClass(latestReading.risk_band)"
        >
          {{ Math.round((latestReading.risk_score ?? 0) * 100) }}% · {{ latestReading.risk_band }}
        </span>
        <span class="text-sm text-ink-soft">
          {{ t('overview.lastAssessed') }}: {{ new Date(latestReading.created_at).toLocaleDateString() }}
        </span>
        <span class="text-sm text-ink-soft">{{ history.length }} {{ t('overview.totalAssessments').toLowerCase() }}</span>
      </div>
    </div>

    <div class="grid sm:grid-cols-2 gap-3">
      <NuxtLink :to="`/assess/${patientId}/record`" class="bg-white border border-mist rounded-2xl p-5 hover:border-teal-600/50 transition-colors">
        <h3 class="font-display text-lg font-medium text-ink mb-1">{{ t('overview.recordCta') }}</h3>
        <p class="text-sm text-ink-soft">{{ t('overview.recordCtaDesc') }}</p>
      </NuxtLink>

      <NuxtLink :to="`/assess/${patientId}/report`" class="bg-teal-600 hover:bg-teal-700 transition-colors rounded-2xl p-5 text-white">
        <h3 class="font-display text-lg font-medium mb-1">{{ t('overview.reportCta') }}</h3>
        <p class="text-sm text-teal-50">{{ t('overview.reportCtaDesc') }}</p>
      </NuxtLink>

      <NuxtLink :to="`/assess/${patientId}/history`" class="bg-white border border-mist rounded-2xl p-5 hover:border-teal-600/50 transition-colors">
        <h3 class="font-display text-lg font-medium text-ink mb-1">{{ t('overview.historyCta') }}</h3>
        <p class="text-sm text-ink-soft">{{ t('overview.historyCtaDesc') }}</p>
      </NuxtLink>

      <NuxtLink :to="`/assess/${patientId}/details`" class="bg-white border border-mist rounded-2xl p-5 hover:border-teal-600/50 transition-colors">
        <h3 class="font-display text-lg font-medium text-ink mb-1">{{ t('overview.detailsCta') }}</h3>
        <p class="text-sm text-ink-soft">{{ t('overview.detailsCtaDesc') }}</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Assessment } from '~/composables/useApi'

const patientId = inject<string>('patientId')!
const api = useApi()
const { t } = useI18n()

const history = ref<Assessment[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    history.value = await api.listPatientAssessments(patientId)
  } finally {
    loading.value = false
  }
})

const latestReading = computed(() => {
  const scored = history.value.filter((a) => a.task === 'reading' && a.risk_score !== null)
  return scored[scored.length - 1] || null
})

function bandBadgeClass(band: string | null) {
  if (band === 'elevated') return 'bg-rust-100 text-rust-600'
  if (band === 'moderate') return 'bg-gold-100 text-gold-600'
  return 'bg-teal-50 text-teal-600'
}
</script>
