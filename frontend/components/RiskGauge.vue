<!--
  The "cadence pulse" -- an arc gauge that reads the risk score the way the rest
  of the product reads voice: as a rhythm. The tick marks along the arc echo the
  waveform bars in Recorder.vue, so the result screen and the recording screen
  share one visual language instead of the gauge being a bolted-on chart.
-->
<template>
  <div class="flex flex-col items-center gap-3">
    <svg viewBox="0 0 200 120" class="w-56 h-auto">
      <!-- background ticks -->
      <g v-for="i in 41" :key="i">
        <line
          :x1="tickPos(i).x1" :y1="tickPos(i).y1" :x2="tickPos(i).x2" :y2="tickPos(i).y2"
          :stroke="i / 41 <= score ? bandColor : 'var(--color-mist)'"
          stroke-width="3" stroke-linecap="round"
        />
      </g>
      <text x="100" y="95" text-anchor="middle" class="font-display" :fill="bandColor" style="font-size: 34px; font-weight: 500;">
        {{ pct }}%
      </text>
    </svg>
    <span
      class="px-3 py-1 rounded-full text-xs font-semibold tracking-wide uppercase"
      :style="{ background: bandBg, color: bandColor }"
    >
      {{ band }} range
    </span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ score: number; band: string }>()

const pct = computed(() => Math.round(props.score * 100))

const bandColor = computed(() => {
  if (props.band === 'elevated') return 'var(--color-rust-600)'
  if (props.band === 'moderate') return 'var(--color-gold-600)'
  return 'var(--color-teal-600)'
})
const bandBg = computed(() => {
  if (props.band === 'elevated') return 'var(--color-rust-100)'
  if (props.band === 'moderate') return 'var(--color-gold-100)'
  return 'var(--color-teal-50)'
})

// Lay 41 ticks along a semicircular arc (180deg), radius 80, center (100,100).
function tickPos(i: number) {
  const t = (i - 1) / 40
  const angle = Math.PI - t * Math.PI // 180deg (left) -> 0deg (right)
  const cx = 100, cy = 100, rOuter = 80, rInner = 68
  return {
    x1: cx + rOuter * Math.cos(angle),
    y1: cy - rOuter * Math.sin(angle),
    x2: cx + rInner * Math.cos(angle),
    y2: cy - rInner * Math.sin(angle),
  }
}
</script>
