<!--
  Public landing page. Anyone signed out lands here (see middleware/auth.global.ts)
  instead of going straight to the sign-in form -- a short, calm intro before the
  clinician console rather than a bare login box as the front door.
-->
<template>
  <div class="min-h-[72vh] flex flex-col items-center justify-center text-center px-2 py-8 sm:py-14">
    <div class="rise" style="animation-delay: 0s">
      <MascotLogo size="xl" />
    </div>

    <h1 class="rise font-display text-3xl sm:text-4xl font-medium text-ink mt-6 mb-3 max-w-lg" style="animation-delay: 0.08s">
      {{ t('welcome.headline') }}
    </h1>

    <p class="rise text-ink-soft max-w-sm mb-1" style="animation-delay: 0.16s">
      {{ t('welcome.subhead') }}
    </p>
    <p class="rise text-teal-600 text-sm font-semibold mb-9" style="animation-delay: 0.22s">
      {{ t('welcome.tagline') }}
    </p>

    <NuxtLink
      to="/login"
      class="rise rounded-full bg-teal-600 hover:bg-teal-700 text-white font-semibold px-9 py-3.5 text-base transition-colors shadow-sm shadow-teal-900/10"
      style="animation-delay: 0.3s"
    >
      {{ t('welcome.cta') }}
    </NuxtLink>

    <p class="rise text-xs text-ink-soft/70 mt-10 max-w-xs" style="animation-delay: 0.38s">
      {{ t('welcome.footnote') }}
    </p>

    <div class="rise mt-6" style="animation-delay: 0.44s">
      <LanguageToggle />
    </div>
  </div>
</template>

<script setup lang="ts">
const { t, initLocale } = useI18n()
initLocale()
</script>

<style scoped>
.rise {
  animation: welcome-rise 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes welcome-rise {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
