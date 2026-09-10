<!--
  Parent layout for everything about one patient. Fetches the patient + current
  clinician ONCE here and provides them to every child route, instead of each
  sub-page re-fetching independently. Renders a small set of destination links
  (Overview / Record / History & Trends / Report / Details) rather than the old
  single page with six inline tab buttons -- each destination is now its own
  focused page with its own URL, which also means "send a neurologist a link to
  this patient's report" is now a real, bookmarkable thing.
-->
<template>
  <div v-if="loadError" class="bg-white border border-rust-100 rounded-2xl p-6 text-rust-600 text-sm">
    {{ loadError }}
  </div>
  <div v-else-if="!patient" class="text-ink-soft text-sm">Loading patient…</div>
  <div v-else>
    <NuxtLink to="/" class="text-sm text-teal-600 hover:text-teal-700 font-medium mb-3 inline-block print:hidden">
      ← {{ t('assess.backToDashboard') }}
    </NuxtLink>
    <h1 class="font-display text-3xl font-medium text-ink mb-1">{{ patient.display_id }}</h1>
    <p class="text-ink-soft mb-5">
      {{ patient.facility || 'No facility on file' }} · {{ (patient.language || 'en').toUpperCase() }}
      <span v-if="patient.age"> · {{ patient.age }}y</span>
    </p>

    <nav class="flex gap-2 mb-6 flex-wrap print:hidden">
      <NuxtLink
        v-for="item in navItems" :key="item.to" :to="item.to"
        class="rounded-full px-4 py-2 text-sm font-medium border transition-colors"
        :class="isActive(item.to)
          ? 'bg-teal-600 text-white border-teal-600'
          : 'bg-white text-ink-soft border-mist hover:border-teal-600/50'"
      >
        {{ t(item.labelKey) }}
      </NuxtLink>
    </nav>

    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import type { ClinicianMe, Patient } from '~/composables/useApi'

const route = useRoute()
const api = useApi()
const patientId = route.params.patientId as string
const { t } = useI18n()

const patient = ref<Patient | null>(null)
const me = ref<ClinicianMe | null>(null)
const loadError = ref<string | null>(null)

// Shared with every child route under /assess/[patientId]/* -- see e.g.
// pages/assess/[patientId]/record.vue for the inject() side.
provide('patientId', patientId)
provide('patient', patient)
provide('me', me)
provide('refetchPatient', async () => { patient.value = await api.getPatient(patientId) })

onMounted(async () => {
  try {
    const [p, m] = await Promise.all([api.getPatient(patientId), api.getMe()])
    patient.value = p
    me.value = m
  } catch (e: any) {
    loadError.value = e?.data?.detail || 'Could not load this patient.'
  }
})

const navItems = [
  { to: `/assess/${patientId}`, labelKey: 'assess.nav.overview' },
  { to: `/assess/${patientId}/record`, labelKey: 'assess.nav.record' },
  ...(useRuntimeConfig().public.voiceIntelligenceEnabled ? [{ to: `/assess/${patientId}/voice-intelligence`, labelKey: 'assess.nav.voiceIntelligence' }] : []),
  { to: `/assess/${patientId}/history`, labelKey: 'assess.nav.history' },
  { to: `/assess/${patientId}/report`, labelKey: 'assess.nav.report' },
  { to: `/assess/${patientId}/details`, labelKey: 'assess.nav.details' },
]

function isActive(to: string) {
  return to.endsWith(`/${patientId}`) ? route.path === to : route.path.startsWith(to)
}
</script>
