<!--
  A small hand-drawn SVG trend line -- deliberately not a charting library, to
  match RiskGauge's visual language rather than bolting on a generic chart. Dots
  are colored by risk band when available (so a risk-score trend reads the same
  teal/gold/rust language as the gauge); a plain biomarker series just uses `color`.
-->
<template>
  <svg :viewBox="`0 0 ${width} ${height}`" class="w-full h-auto">
    <line
      v-for="(gl, i) in gridY" :key="'g' + i"
      :x1="padL" :x2="width - padR" :y1="gl.y" :y2="gl.y"
      stroke="var(--color-mist)" stroke-width="1"
    />
    <text
      v-for="(gl, i) in gridY" :key="'gt' + i"
      :x="padL - 8" :y="gl.y + 3" text-anchor="end"
      class="font-mono" style="font-size: 10px" fill="var(--color-ink-soft)"
    >{{ gl.label }}</text>

    <polyline
      :points="linePoints" fill="none" :stroke="lineColor"
      stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
    />

    <circle
      v-for="(p, i) in scaled" :key="'c' + i"
      :cx="p.x" :cy="p.y" r="4" :fill="dotColor(points[i])"
      stroke="white" stroke-width="1.5"
    />

    <text :x="padL" :y="height - 4" text-anchor="start" class="font-mono" style="font-size: 10px" fill="var(--color-ink-soft)">
      {{ firstLabel }}
    </text>
    <text :x="width - padR" :y="height - 4" text-anchor="end" class="font-mono" style="font-size: 10px" fill="var(--color-ink-soft)">
      {{ lastLabel }}
    </text>
  </svg>
</template>

<script setup lang="ts">
const props = defineProps<{
  points: { date: string; value: number; band?: string | null }[]
  color?: string
}>()

const width = 600
const height = 170
const padL = 34
const padR = 10
const padT = 14
const padB = 22

const values = computed(() => props.points.map((p) => p.value))
const minV = computed(() => Math.min(...values.value))
const maxV = computed(() => Math.max(...values.value))
const range = computed(() => maxV.value - minV.value || Math.abs(maxV.value) * 0.1 || 1)

// Pad the value range so a flat or near-flat series doesn't hug an edge.
const yMin = computed(() => minV.value - range.value * 0.2)
const yMax = computed(() => maxV.value + range.value * 0.2)

function xFor(i: number) {
  if (props.points.length <= 1) return padL + (width - padL - padR) / 2
  return padL + (i / (props.points.length - 1)) * (width - padL - padR)
}
function yFor(v: number) {
  const span = yMax.value - yMin.value || 1
  const t = (v - yMin.value) / span
  return height - padB - t * (height - padT - padB)
}

const scaled = computed(() => props.points.map((p, i) => ({ x: xFor(i), y: yFor(p.value) })))
const linePoints = computed(() => scaled.value.map((p) => `${p.x},${p.y}`).join(' '))

const gridY = computed(() => {
  const steps = 3
  return Array.from({ length: steps + 1 }, (_, i) => {
    const v = yMin.value + (i / steps) * (yMax.value - yMin.value)
    return { y: yFor(v), label: v >= 100 ? Math.round(v).toString() : v.toFixed(v < 1 ? 2 : 1) }
  })
})

const lineColor = computed(() => props.color || 'var(--color-teal-600)')

function dotColor(p: { band?: string | null }) {
  if (p.band === 'elevated') return 'var(--color-rust-600)'
  if (p.band === 'moderate') return 'var(--color-gold-600)'
  if (p.band === 'low') return 'var(--color-teal-600)'
  return lineColor.value
}

function fmtDate(d: string) {
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}
const firstLabel = computed(() => (props.points.length ? fmtDate(props.points[0].date) : ''))
const lastLabel = computed(() => (props.points.length ? fmtDate(props.points[props.points.length - 1].date) : ''))
</script>
