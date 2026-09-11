<!--
  An original illustration for the "why voice" science section -- deliberately
  NOT a stock photo of a real person with Parkinson's. Two reasons: depicting an
  identifiable individual's real medical condition without their consent isn't
  something to source from a generic image search for a product page, and even
  a properly-licensed stock photo of "a sick person" tends to read as slightly
  exploitative in a clinical product rather than explanatory. This instead shows
  the actual MECHANISM the section is explaining -- a hand-tremor motion path
  paired with a voice waveform -- which is more informative than a photo would
  be anyway: it's illustrating the signal, not just gesturing at illness.
-->
<template>
  <svg viewBox="0 0 340 300" class="w-full h-auto max-w-sm mx-auto" aria-hidden="true">
    <ellipse cx="170" cy="275" rx="110" ry="12" fill="var(--color-ink)" opacity="0.06" />

    <!-- simplified seated figure -->
    <g>
      <circle cx="150" cy="70" r="34" fill="var(--color-teal-100)" />
      <path d="M108 260 C104 190 112 150 150 138 C188 150 196 190 192 260 Z" fill="var(--color-teal-700)" />
      <path d="M150 138 C170 142 184 158 190 182 L120 182 C124 158 136 144 150 138 Z" fill="var(--color-teal-700)" opacity="0.35" />
    </g>

    <!-- tremor path: the hand's motion traced as a shaky arc, labeled subtly -->
    <g stroke="var(--color-rust-600)" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.85">
      <path d="M188 200 C196 194 182 188 194 182 C204 176 190 170 200 164 C210 158 198 150 206 144" />
    </g>
    <circle cx="206" cy="144" r="5" fill="var(--color-rust-600)" />

    <!-- voice waveform rising from the figure, same bars used everywhere else -->
    <g transform="translate(210, 60)">
      <rect x="0" y="34" width="6" height="16" rx="3" fill="var(--color-teal-600)" />
      <rect x="10" y="20" width="6" height="44" rx="3" fill="var(--color-gold-600)" />
      <rect x="20" y="28" width="6" height="28" rx="3" fill="var(--color-teal-600)" />
      <rect x="30" y="8" width="6" height="68" rx="3" fill="var(--color-teal-700)" />
      <rect x="40" y="22" width="6" height="40" rx="3" fill="var(--color-gold-600)" />
      <rect x="50" y="32" width="6" height="20" rx="3" fill="var(--color-teal-600)" />
    </g>
  </svg>
</template>
