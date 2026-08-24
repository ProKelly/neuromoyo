<!--
  Neuromoyo wordmark. The mark is a small waveform pulse -- the same motif used
  live in Recorder.vue and as the tick-arc in RiskGauge.vue -- so the brand mark,
  the recording feedback, and the result gauge all read as one visual idea
  instead of the logo being an unrelated decoration.
-->
<template>
  <div class="flex items-center gap-2" :class="stacked ? 'flex-col items-start gap-1' : ''">
    <svg viewBox="0 0 32 32" :class="markSize" aria-hidden="true">
      <rect x="0" y="0" width="32" height="32" rx="9" fill="var(--color-teal-600)" />
      <rect x="7" y="14" width="2.4" height="4" rx="1.2" fill="var(--color-teal-100)" />
      <rect x="11.5" y="9" width="2.4" height="14" rx="1.2" fill="var(--color-teal-100)" />
      <rect x="16" y="6" width="2.4" height="20" rx="1.2" fill="white" />
      <rect x="20.5" y="10" width="2.4" height="12" rx="1.2" fill="var(--color-teal-100)" />
      <rect x="25" y="13" width="2.4" height="6" rx="1.2" fill="var(--color-teal-100)" />
    </svg>
    <div class="flex items-baseline gap-2" :class="stacked ? 'flex-col items-start gap-0' : ''">
      <span class="font-display font-medium text-ink tracking-tight" :class="textSize">Neuromoyo</span>
      <span v-if="showTagline" class="text-teal-600 text-sm font-medium">NeuroVoice</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{ size?: 'sm' | 'md' | 'lg'; showTagline?: boolean; stacked?: boolean }>(),
  { size: 'md', showTagline: true, stacked: false }
)

const markSize = computed(() => ({ sm: 'w-6 h-6', md: 'w-8 h-8', lg: 'w-11 h-11' }[props.size]))
const textSize = computed(() => ({ sm: 'text-base', md: 'text-xl', lg: 'text-3xl' }[props.size]))
</script>
