<!--
  Public landing page. Anyone signed out lands here (see middleware/auth.global.ts)
  instead of going straight to the sign-in form. Full-bleed sections (app.vue
  gives this route the full viewport width, unlike every console page which
  stays inside the standard max-w-3xl column) -- each section picks its own
  inner max-width, standard marketing-page pattern.
-->
<template>
  <div>
    <!-- Hero -->
    <section class="min-h-[72vh] flex flex-col items-center justify-center text-center px-4 py-8 sm:py-14">
      <div class="rise" style="animation-delay: 0s">
        <MascotLogo size="xl" />
      </div>

      <p class="rise text-xs font-semibold tracking-wide uppercase text-teal-600 mt-6 mb-3" style="animation-delay: 0.05s">
        {{ t('welcome.eyebrow') }}
      </p>

      <h1 class="rise font-display text-3xl sm:text-4xl font-medium text-ink mb-3 max-w-lg" style="animation-delay: 0.08s">
        {{ t('welcome.headline') }}
      </h1>

      <p class="rise text-ink-soft max-w-sm mb-1" style="animation-delay: 0.16s">
        {{ t('welcome.subhead') }}
      </p>
      <p class="rise text-teal-600 text-sm font-semibold mb-9" style="animation-delay: 0.22s">
        {{ t('welcome.tagline') }}
      </p>

      <div class="rise flex flex-col items-center gap-4" style="animation-delay: 0.3s">
        <NuxtLink
          to="/login"
          class="rounded-full bg-teal-600 hover:bg-teal-700 text-white font-semibold px-9 py-3.5 text-base transition-colors shadow-sm shadow-teal-900/10"
        >
          {{ t('welcome.cta') }}
        </NuxtLink>
        <a href="#science" class="text-sm font-medium text-ink-soft hover:text-teal-600 transition-colors">
          {{ t('welcome.secondaryCta') }} ↓
        </a>
      </div>

      <p class="rise text-xs text-ink-soft/70 mt-10 max-w-xs" style="animation-delay: 0.38s">
        {{ t('welcome.footnote') }}
      </p>
    </section>

    <!-- How it works -->
    <section class="border-t border-mist bg-white/60 py-14 sm:py-16 px-4">
      <div class="max-w-3xl mx-auto">
        <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2 text-center">
          {{ t('welcome.how.eyebrow') }}
        </p>
        <h2 class="font-display text-2xl sm:text-3xl font-medium text-ink text-center mb-10 max-w-md mx-auto">
          {{ t('welcome.how.heading') }}
        </h2>
        <div class="grid sm:grid-cols-3 gap-4">
          <div v-for="(step, i) in howSteps" :key="i" class="bg-white border border-mist rounded-2xl p-5">
            <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-teal-50 text-teal-600 font-mono text-sm font-semibold mb-3">
              {{ i + 1 }}
            </span>
            <h3 class="font-display text-base font-medium text-ink mb-1.5">{{ t(step.titleKey) }}</h3>
            <p class="text-sm text-ink-soft leading-relaxed">{{ t(step.descKey) }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- The science -->
    <section id="science" class="border-t border-mist py-14 sm:py-16 px-4 scroll-mt-16">
      <div class="max-w-3xl mx-auto">
        <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2 text-center">
          {{ t('welcome.science.eyebrow') }}
        </p>
        <h2 class="font-display text-2xl sm:text-3xl font-medium text-ink text-center mb-10 max-w-lg mx-auto">
          {{ t('welcome.science.heading') }}
        </h2>

        <div class="bg-white border border-mist rounded-2xl p-6 sm:p-8 mb-6">
          <p class="text-ink leading-relaxed">{{ t('welcome.science.p1') }}</p>
        </div>

        <div class="grid sm:grid-cols-[1fr_1.3fr] gap-6 sm:gap-8 items-center bg-white border border-mist rounded-2xl p-6 sm:p-8 mb-6">
          <div>
            <VoiceSymptomIllustration />
            <p class="text-xs text-ink-soft text-center mt-3 italic">{{ t('welcome.science.illustrationCaption') }}</p>
          </div>
          <p class="text-ink leading-relaxed">{{ t('welcome.science.p2') }}</p>
        </div>

        <div class="bg-white border border-mist rounded-2xl p-6 sm:p-8 mb-2">
          <p class="text-ink leading-relaxed mb-4">{{ t('welcome.science.p3') }}</p>
          <p class="text-ink leading-relaxed">{{ t('welcome.science.p4') }}</p>
        </div>
        <p class="text-xs text-ink-soft/80 px-1">{{ t('welcome.science.sources') }}</p>
      </div>
    </section>

    <!-- Built for Africa -->
    <section class="border-t border-mist bg-white/60 py-14 sm:py-16 px-4">
      <div class="max-w-3xl mx-auto">
        <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2 text-center">
          {{ t('welcome.africa.eyebrow') }}
        </p>
        <h2 class="font-display text-2xl sm:text-3xl font-medium text-ink text-center mb-10 max-w-lg mx-auto">
          {{ t('welcome.africa.heading') }}
        </h2>
        <div class="grid sm:grid-cols-3 gap-4">
          <div v-for="(item, i) in africaItems" :key="i" class="bg-white border border-mist rounded-2xl p-5">
            <h3 class="font-display text-base font-medium text-ink mb-1.5">{{ t(item.titleKey) }}</h3>
            <p class="text-sm text-ink-soft leading-relaxed">{{ t(item.descKey) }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="border-t border-mist py-14 sm:py-16 px-4 text-center">
      <h2 class="font-display text-2xl sm:text-3xl font-medium text-ink mb-6 max-w-sm mx-auto">
        {{ t('welcome.finalCta.heading') }}
      </h2>
      <NuxtLink
        to="/login"
        class="inline-block rounded-full bg-teal-600 hover:bg-teal-700 text-white font-semibold px-9 py-3.5 text-base transition-colors shadow-sm shadow-teal-900/10 mb-6"
      >
        {{ t('welcome.cta') }}
      </NuxtLink>
      <div>
        <LanguageToggle />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t, initLocale } = useI18n()
initLocale()

const howSteps = [
  { titleKey: 'welcome.how.step1.title', descKey: 'welcome.how.step1.desc' },
  { titleKey: 'welcome.how.step2.title', descKey: 'welcome.how.step2.desc' },
  { titleKey: 'welcome.how.step3.title', descKey: 'welcome.how.step3.desc' },
]

const africaItems = [
  { titleKey: 'welcome.africa.item1.title', descKey: 'welcome.africa.item1.desc' },
  { titleKey: 'welcome.africa.item2.title', descKey: 'welcome.africa.item2.desc' },
  { titleKey: 'welcome.africa.item3.title', descKey: 'welcome.africa.item3.desc' },
]
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
