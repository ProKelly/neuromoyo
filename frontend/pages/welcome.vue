<!-- pages/welcome.vue -->
<template>
  <div class="min-h-[100vh] flex flex-col">
    <!-- Hero Section -->
    <section class="relative flex-1 flex items-center justify-center px-4 py-12 sm:py-20 overflow-hidden">
      <!-- Subtle pattern background -->
      <div class="absolute inset-0 pointer-events-none opacity-[0.03]">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 30% 40%, #0d9488 1px, transparent 1px); background-size: 24px 24px;"></div>
      </div>
      
      <!-- Decorative corner accents -->
      <div class="absolute top-0 right-0 w-64 h-64 pointer-events-none opacity-[0.04]">
        <div class="absolute inset-0" style="background: radial-gradient(circle at 100% 0%, #0d9488, transparent 70%);"></div>
      </div>
      <div class="absolute bottom-0 left-0 w-64 h-64 pointer-events-none opacity-[0.04]">
        <div class="absolute inset-0" style="background: radial-gradient(circle at 0% 100%, #0d9488, transparent 70%);"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto text-center">
        <div class="rise" style="animation-delay: 0s">
          <MascotLogo size="xl" />
        </div>

        <h1 class="rise font-display text-4xl sm:text-5xl md:text-6xl font-medium text-ink mt-6 mb-4 max-w-3xl mx-auto leading-tight" style="animation-delay: 0.08s">
          {{ t('welcome.headline') }}
        </h1>

        <p class="rise text-lg sm:text-xl text-ink-soft max-w-2xl mx-auto mb-2 leading-relaxed" style="animation-delay: 0.16s">
          {{ t('welcome.subhead') }}
        </p>
        <p class="rise text-teal-600 text-base font-semibold mb-10" style="animation-delay: 0.22s">
          {{ t('welcome.tagline') }}
        </p>

        <div class="rise flex flex-col sm:flex-row items-center justify-center gap-4" style="animation-delay: 0.3s">
          <NuxtLink
            to="/login"
            class="rounded-full bg-teal-600 hover:bg-teal-700 text-white font-semibold px-10 py-4 text-base transition-all shadow-lg shadow-teal-900/15 hover:shadow-teal-900/25 hover:-translate-y-0.5"
          >
            {{ t('welcome.cta') }}
          </NuxtLink>
          <a
            href="#science"
            class="rounded-full border-2 border-mist hover:border-teal-600/50 text-ink-soft hover:text-teal-600 font-medium px-8 py-4 text-base transition-all"
          >
            Learn more ↓
          </a>
        </div>

        <p class="rise text-xs text-ink-soft/70 mt-8 max-w-xs mx-auto" style="animation-delay: 0.38s">
          {{ t('welcome.footnote') }}
        </p>

        <div class="rise mt-4" style="animation-delay: 0.44s">
          <LanguageToggle />
        </div>
      </div>
    </section>

    <!-- Science Section -->
    <section id="science" class="relative py-16 sm:py-24 bg-white/50 border-t border-mist">
      <!-- Subtle pattern -->
      <div class="absolute inset-0 pointer-events-none opacity-[0.02]">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 20% 30%, #0d9488 1px, transparent 1px); background-size: 30px 30px;"></div>
      </div>

      <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6">
        <div class="text-center mb-12">
          <span class="text-xs font-semibold tracking-widest uppercase text-teal-600">The Science</span>
          <h2 class="font-display text-3xl sm:text-4xl font-medium text-ink mt-2">Early detection through voice</h2>
          <p class="text-ink-soft max-w-2xl mx-auto mt-3">How vocal biomarkers are transforming Parkinson's disease screening</p>
        </div>

        <div class="grid md:grid-cols-2 gap-8 lg:gap-12 items-center">
          <!-- Image Column -->
          <div class="order-2 md:order-1">
            <div class="relative rounded-2xl overflow-hidden shadow-lg border border-mist bg-white">
              <img
                src="https://images.unsplash.com/photo-1581579438747-1dc8d17bbce4?w=800&h=600&fit=crop&crop=center"
                alt="Neurological examination and Parkinson's disease awareness"
                class="w-full h-auto object-cover"
                loading="lazy"
              />
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
                <p class="text-white text-xs font-medium">Early neurological assessment can identify subtle voice changes years before motor symptoms appear</p>
              </div>
            </div>
            <div class="mt-4 flex items-center gap-3 text-xs text-ink-soft">
              <span class="flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                Peer-reviewed research
              </span>
              <span class="flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                Clinical validation
              </span>
            </div>
          </div>

          <!-- Content Column -->
          <div class="order-1 md:order-2 space-y-6">
            <div class="bg-white border border-mist rounded-xl p-6 shadow-sm">
              <div class="flex items-start gap-4">
                <div class="shrink-0 w-10 h-10 rounded-full bg-teal-50 flex items-center justify-center">
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-ink">The Parkinson's challenge in Africa</h3>
                  <p class="text-sm text-ink-soft leading-relaxed mt-1">
                    Parkinson's disease affects over 10 million people worldwide, with cases in Africa projected to double by 2030. 
                    Limited access to neurologists means <span class="font-medium text-ink">up to 80% of cases go undiagnosed</span> until 
                    significant motor impairment has already occurred.
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-mist rounded-xl p-6 shadow-sm">
              <div class="flex items-start gap-4">
                <div class="shrink-0 w-10 h-10 rounded-full bg-teal-50 flex items-center justify-center">
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-ink">Voice as a window to the brain</h3>
                  <p class="text-sm text-ink-soft leading-relaxed mt-1">
                    <span class="font-medium text-ink">Scientific research</span> has established that vocal changes — 
                    including reduced pitch variability, slower speech rate, and vocal tremor — can appear 
                    <span class="font-medium text-ink">5-10 years before</span> classic motor symptoms like tremor or rigidity. 
                    These changes are detectable through acoustic analysis with <span class="font-medium text-ink">>90% sensitivity</span> 
                    in clinical studies.
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-teal-50 border border-teal-100 rounded-xl p-6">
              <div class="flex items-start gap-4">
                <div class="shrink-0 w-10 h-10 rounded-full bg-teal-600 flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-ink">Our solution: AI-powered early warning</h3>
                  <p class="text-sm text-ink leading-relaxed mt-1">
                    NeuroMonitor uses <span class="font-medium text-teal-700">machine learning models</span> trained on thousands 
                    of voice samples to detect subtle acoustic patterns associated with early Parkinson's. 
                    Our system provides <span class="font-medium text-teal-700">real-time risk assessment</span> during routine 
                    clinical visits — no specialist equipment or lengthy testing required.
                  </p>
                  <div class="mt-3 flex flex-wrap gap-3">
                    <span class="text-xs bg-white/80 px-3 py-1 rounded-full border border-teal-100 text-ink-soft">
                      ✓ Validated on African populations
                    </span>
                    <span class="text-xs bg-white/80 px-3 py-1 rounded-full border border-teal-100 text-ink-soft">
                      ✓ Works with any smartphone
                    </span>
                    <span class="text-xs bg-white/80 px-3 py-1 rounded-full border border-teal-100 text-ink-soft">
                      ✓ Offline-capable
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Section -->
        <div class="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 border-t border-mist pt-12">
          <div class="text-center">
            <p class="text-3xl font-display font-medium text-teal-600">10M+</p>
            <p class="text-xs text-ink-soft mt-1">Living with Parkinson's globally</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-display font-medium text-teal-600">5-10y</p>
            <p class="text-xs text-ink-soft mt-1">Early voice changes precede motor symptoms</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-display font-medium text-teal-600">90%</p>
            <p class="text-xs text-ink-soft mt-1">Sensitivity in clinical voice analysis studies</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-display font-medium text-teal-600">2x</p>
            <p class="text-xs text-ink-soft mt-1">Projected increase in African cases by 2030</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="relative py-16 sm:py-20 bg-mist/30 border-t border-mist">
      <div class="absolute inset-0 pointer-events-none opacity-[0.02]">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 70% 60%, #0d9488 1px, transparent 1px); background-size: 20px 20px;"></div>
      </div>

      <div class="relative z-10 max-w-5xl mx-auto px-4 sm:px-6">
        <div class="text-center mb-12">
          <span class="text-xs font-semibold tracking-widest uppercase text-teal-600">How it works</span>
          <h2 class="font-display text-3xl sm:text-4xl font-medium text-ink mt-2">Simple, fast, accessible</h2>
        </div>

        <div class="grid sm:grid-cols-3 gap-6">
          <div class="bg-white border border-mist rounded-xl p-6 text-center hover:border-teal-600/30 transition-all shadow-sm hover:shadow-md">
            <div class="w-14 h-14 rounded-full bg-teal-50 flex items-center justify-center mx-auto mb-4">
              <svg class="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              </svg>
            </div>
            <h3 class="font-semibold text-ink mb-1">1. Record voice</h3>
            <p class="text-sm text-ink-soft">Patient reads a passage or produces vocal tasks using any smartphone or microphone</p>
          </div>

          <div className="bg-white border border-mist rounded-xl p-6 text-center hover:border-teal-600/30 transition-all shadow-sm hover:shadow-md">
            <div className="w-14 h-14 rounded-full bg-teal-50 flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
            <h3 className="font-semibold text-ink mb-1">2. AI analysis</h3>
            <p className="text-sm text-ink-soft">Our ML models extract acoustic biomarkers and compute risk scores in real time</p>
          </div>

          <div className="bg-white border border-mist rounded-xl p-6 text-center hover:border-teal-600/30 transition-all shadow-sm hover:shadow-md">
            <div className="w-14 h-14 rounded-full bg-teal-50 flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 className="font-semibold text-ink mb-1">3. Clinical action</h3>
            <p className="text-sm text-ink-soft">Clear risk bands and recommendations guide clinical decision-making and referrals</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Footer -->
    <section className="relative py-12 bg-white border-t border-mist">
      <div className="relative z-10 max-w-3xl mx-auto px-4 text-center">
        <h2 className="font-display text-2xl sm:text-3xl font-medium text-ink mb-3">Ready to start screening?</h2>
        <p className="text-ink-soft mb-6">Join clinicians across Africa using NeuroMonitor for early Parkinson's detection</p>
        <NuxtLink
          to="/login"
          className="inline-block rounded-full bg-teal-600 hover:bg-teal-700 text-white font-semibold px-10 py-3.5 text-base transition-all shadow-lg shadow-teal-900/15 hover:shadow-teal-900/25 hover:-translate-y-0.5"
        >
          Get started
        </NuxtLink>
        <p className="text-xs text-ink-soft/70 mt-4">Free for pilot sites · No equipment required</p>
      </div>
    </section>
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