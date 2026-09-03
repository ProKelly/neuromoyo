<!--
  A very quiet, app-wide texture -- tiny waveform-tick clusters (the same motif
  as Recorder.vue's live meter, RiskGauge.vue, TrendChart.vue, and the logos),
  tiled sparsely at low opacity. Fixed behind everything, non-interactive.

  Deliberately subtle: every card in this app has a solid white background, so
  the pattern only shows in the paper-colored gutters between cards -- texture
  in the negative space, never behind anything a clinician needs to read. This
  is the one thing that has to stay true no matter how the pattern itself
  changes later: it must never reduce contrast on real content.
-->
<template>
  <svg class="fixed inset-0 -z-10 w-full h-full pointer-events-none print:hidden" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
    <defs>
      <pattern id="neuromoyo-bg-ticks" width="72" height="72" patternUnits="userSpaceOnUse">
        <g opacity="0.05">
          <rect x="8" y="30" width="3" height="8" rx="1.5" fill="var(--color-teal-900)" />
          <rect x="14" y="24" width="3" height="20" rx="1.5" fill="var(--color-teal-900)" />
          <rect x="20" y="32" width="3" height="6" rx="1.5" fill="var(--color-teal-900)" />
        </g>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#neuromoyo-bg-ticks)" />
  </svg>
</template>
