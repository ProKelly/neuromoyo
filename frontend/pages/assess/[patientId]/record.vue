<template>
  <div>
    <nav class="flex gap-2 mb-5 flex-wrap">
      <button
        v-for="taskItem in taskTabs" :key="taskItem.id"
        class="rounded-full px-4 py-2 text-sm font-medium border transition-colors cursor-pointer"
        :class="task === taskItem.id
          ? 'bg-teal-600 text-white border-teal-600'
          : 'bg-white text-ink-soft border-mist hover:border-teal-600/50'"
        @click="task = taskItem.id; result = null"
      >
        {{ t(taskItem.labelKey) }}
      </button>
    </nav>

    <section v-if="task === 'reading'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Reading passage</h2>
      <p class="text-sm text-ink-soft mb-4">Read the passage aloud, clearly, for about 30 seconds.</p>
      <p class="leading-relaxed text-ink bg-paper rounded-xl p-4 mb-5 border border-mist">{{ passageText }}</p>
      <Recorder @recorded="(b) => submit('reading', b)" />
    </section>

    <section v-if="task === 'vowel'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Sustained vowel</h2>
      <p class="text-sm text-ink-soft mb-5">Take a breath and hold a steady "aaah" for 5–10 seconds.</p>
      <Recorder @recorded="(b) => submit('vowel', b)" />
    </section>

    <section v-if="task === 'ddk'" class="bg-white border border-mist rounded-2xl p-6 mb-6">
      <h2 class="font-display text-xl font-medium text-ink mb-1">Diadochokinetic (/pa-ta-ka/)</h2>
      <p class="text-sm text-ink-soft mb-5">Repeat "pa-ta-ka" as fast and evenly as possible for about 5 seconds.</p>
      <Recorder @recorded="(b) => submit('ddk', b)" />
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

        <NuxtLink
          :to="`/assess/${patientId}`"
          class="inline-block mt-5 text-sm font-medium text-teal-600 hover:text-teal-700"
        >
          ← Back to overview
        </NuxtLink>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Patient, ScreenResult } from '~/composables/useApi'
import passages from '~/assets/passages.json'

const patientId = inject<string>('patientId')!
const patient = inject<Ref<Patient | null>>('patient')!
const api = useApi()
const { t } = useI18n()

const taskTabs = [
  { id: 'reading', labelKey: 'assess.tab.reading' },
  { id: 'vowel', labelKey: 'assess.tab.vowel' },
  { id: 'ddk', labelKey: 'assess.tab.ddk' },
] as const

const task = ref<typeof taskTabs[number]['id']>('reading')
const submitting = ref(false)
const result = ref<ScreenResult | null>(null)

const passageText = computed(() => {
  const lang = patient.value?.language || 'en'
  return (passages as Record<string, { text: string }>)[lang]?.text
    || (passages as Record<string, { text: string }>).en.text
})

async function submit(t: 'reading' | 'vowel' | 'ddk', blob: Blob) {
  submitting.value = true
  result.value = null
  try {
    if (t === 'reading') result.value = await api.screenReading(patientId, blob)
    if (t === 'vowel') result.value = await api.screenVowel(patientId, blob)
    if (t === 'ddk') result.value = await api.screenDdk(patientId, blob)
  } catch (e: any) {
    const detail = e?.data?.detail || e?.data?.error || e?.message
    result.value = { ok: false, error: detail ? `Analysis failed: ${detail}` : 'Analysis failed. Check the backend connection and try again.', biomarkers: [] }
  } finally {
    submitting.value = false
  }
}
</script>
