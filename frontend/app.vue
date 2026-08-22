<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b border-mist bg-white">
      <div class="max-w-2xl mx-auto px-5 py-4 flex items-baseline gap-2.5">
        <NuxtLink to="/" class="font-display text-xl font-medium text-ink tracking-tight">
          Neuromoyo
        </NuxtLink>
        <span class="text-teal-600 text-sm font-medium">NeuroVoice</span>
      </div>
    </header>
    <main class="flex-1">
      <div class="max-w-2xl mx-auto px-5 py-8 w-full">
        <NuxtPage />
      </div>
    </main>
    <footer class="border-t border-mist py-4">
      <p class="max-w-2xl mx-auto px-5 text-xs text-ink-soft">
        Screening aid only — not a diagnosis. Always refer to a qualified clinician.
      </p>
    </footer>
  </div>
</template>
