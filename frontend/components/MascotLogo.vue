<!--
  Neuromoyo mascot mark. The "ears" are the same waveform-bar language used by
  Recorder.vue's live mic feedback, RiskGauge.vue, and TrendChart.vue -- so this
  reads as the same visual idea as the rest of the console, not a bolted-on
  illustration. Animation is CSS-only (transform/opacity), so the app-wide
  prefers-reduced-motion rule in main.css already disables it for anyone who
  needs that.
-->
<template>
  <div class="mascot-wrap" :class="[`size-${size}`, { 'is-animated': animated }]">
    <svg viewBox="0 0 220 200" class="mascot-svg" aria-hidden="true">
      <defs>
        <linearGradient id="mascotBodyFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--color-teal-600)" />
          <stop offset="100%" stop-color="var(--color-teal-900)" />
        </linearGradient>
        <linearGradient id="mascotSheen" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16" />
          <stop offset="55%" stop-color="#ffffff" stop-opacity="0" />
        </linearGradient>
        <radialGradient id="mascotCheek" cx="35%" cy="35%" r="70%">
          <stop offset="0%" stop-color="var(--color-teal-50)" />
          <stop offset="100%" stop-color="var(--color-teal-100)" />
        </radialGradient>
      </defs>

      <ellipse cx="110" cy="183" rx="54" ry="8" fill="var(--color-ink)" opacity="0.12" />

      <g class="wave-ears">
        <g transform="translate(2,100)">
          <rect class="wave-bar bar-a" x="0" y="-5" width="5" height="10" rx="2.4" fill="var(--color-teal-600)" />
          <rect class="wave-bar bar-b" x="9" y="-12" width="5" height="24" rx="2.4" fill="var(--color-rust-600)" />
          <rect class="wave-bar bar-c" x="18" y="-8" width="5" height="16" rx="2.4" fill="var(--color-teal-600)" />
        </g>
        <g transform="translate(218,100) scale(-1,1)">
          <rect class="wave-bar bar-a" x="0" y="-5" width="5" height="10" rx="2.4" fill="var(--color-teal-600)" />
          <rect class="wave-bar bar-b" x="9" y="-12" width="5" height="24" rx="2.4" fill="var(--color-rust-600)" />
          <rect class="wave-bar bar-c" x="18" y="-8" width="5" height="16" rx="2.4" fill="var(--color-teal-600)" />
        </g>
      </g>

      <g class="mascot-body">
        <path
          d="M110 24 C148 24 176 42 184 76 C190 100 190 130 172 152 C154 174 132 184 110 184
             C88 184 66 174 48 152 C30 130 30 100 36 76 C44 42 72 24 110 24 Z"
          fill="url(#mascotBodyFill)"
        />
        <path
          d="M110 24 C148 24 176 42 184 76 C189 96 190 121 179 141 C176 118 168 84 148 62
             C130 42 104 32 78 34 C90 27 99 24 110 24 Z"
          fill="url(#mascotSheen)"
        />

        <ellipse cx="72" cy="114" rx="12" ry="7.5" fill="url(#mascotCheek)" opacity="0.85" />
        <ellipse cx="148" cy="114" rx="12" ry="7.5" fill="url(#mascotCheek)" opacity="0.85" />

        <g class="mascot-eyes">
          <circle class="eye" cx="86" cy="92" r="9.2" fill="var(--color-ink)" />
          <circle class="eye" cx="134" cy="92" r="9.2" fill="var(--color-ink)" />
          <circle cx="89.3" cy="88.4" r="3" fill="#ffffff" />
          <circle cx="137.3" cy="88.4" r="3" fill="#ffffff" />
          <circle cx="84" cy="95" r="1.4" fill="#ffffff" opacity="0.55" />
          <circle cx="132" cy="95" r="1.4" fill="#ffffff" opacity="0.55" />
        </g>

        <path d="M97 118 Q110 130 123 118" stroke="var(--color-ink)" stroke-width="4.2" stroke-linecap="round" fill="none" />
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ size?: 'sm' | 'md' | 'lg' | 'xl'; animated?: boolean }>(), {
  size: 'lg',
  animated: true,
})
</script>

<style scoped>
.mascot-wrap { display: inline-flex; }
.mascot-svg { display: block; width: 100%; height: auto; }

.size-sm { width: 40px; }
.size-md { width: 72px; }
.size-lg { width: 120px; }
.size-xl { width: 176px; }

/* Gentle breathing float on the whole character */
.is-animated .mascot-body {
  transform-box: fill-box;
  transform-origin: center;
  animation: mascot-float 4.2s ease-in-out infinite;
}

@keyframes mascot-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* The waveform ears pulse like a live signal, echoing Recorder.vue's mic feedback */
.is-animated .wave-bar {
  transform-box: fill-box;
  transform-origin: center;
  animation: mascot-pulse 1.5s ease-in-out infinite;
}
.is-animated .bar-a { animation-delay: 0s; }
.is-animated .bar-b { animation-delay: 0.18s; }
.is-animated .bar-c { animation-delay: 0.36s; }

@keyframes mascot-pulse {
  0%, 100% { transform: scaleY(0.68); }
  50% { transform: scaleY(1.15); }
}

/* An occasional, unhurried blink -- rare enough to read as charming, not busy */
.is-animated .eye {
  transform-box: fill-box;
  transform-origin: center;
  animation: mascot-blink 6.5s ease-in-out infinite;
}

@keyframes mascot-blink {
  0%, 92%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(0.12); }
}
</style>
