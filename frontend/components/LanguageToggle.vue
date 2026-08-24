<!-- Toggles the console's UI language (English/French) -- not the patient's
     recording language, which stays a per-patient field on the intake form. -->
<template>
  <div class="inline-flex rounded-full border border-mist bg-white p-0.5 text-sm font-medium">
    <button
      class="rounded-full px-3 py-1.5 transition-colors cursor-pointer"
      :class="locale === 'en' ? 'bg-teal-600 text-white' : 'text-ink-soft hover:text-ink'"
      @click="setLocale('en')"
    >
      EN
    </button>
    <button
      class="rounded-full px-3 py-1.5 transition-colors cursor-pointer"
      :class="locale === 'fr' ? 'bg-teal-600 text-white' : 'text-ink-soft hover:text-ink'"
      @click="setLocale('fr')"
    >
      FR
    </button>
  </div>
</template>

<script setup lang="ts">
const { locale, setLocale } = useI18n()
</script>
