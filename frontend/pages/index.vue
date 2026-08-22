<template>
  <div>
    <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2">Step 1 of 2</p>
    <h1 class="font-display text-3xl font-medium text-ink mb-1">New assessment</h1>
    <p class="text-ink-soft mb-8">Enter the patient's clinic ID to begin a NeuroVoice screening.</p>

    <form class="bg-white border border-mist rounded-2xl p-6 flex flex-col gap-5" @submit.prevent="onSubmit">
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Patient ID (clinic-assigned)</span>
        <input
          v-model="form.display_id" required placeholder="e.g. BDA-0042"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
      </label>

      <div class="grid grid-cols-2 gap-4">
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Age</span>
          <input
            v-model.number="form.age" type="number" min="0" max="120"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          />
        </label>
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Sex</span>
          <select
            v-model="form.sex"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          >
            <option :value="null">Prefer not to say</option>
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>
        </label>
      </div>

      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Language</span>
        <select
          v-model="form.language"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        >
          <option value="en">English</option>
          <option value="fr">French</option>
        </select>
      </label>

      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Facility</span>
        <input
          v-model="form.facility" placeholder="Clinic / hospital name"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
      </label>

      <label class="flex items-center gap-2.5">
        <input v-model="form.existing_pd_diagnosis" type="checkbox" class="w-4 h-4 rounded border-mist text-teal-600 focus:ring-teal-600" />
        <span class="text-sm text-ink-soft">Existing Parkinson's diagnosis</span>
      </label>

      <button
        type="submit" :disabled="submitting"
        class="mt-1 rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3 transition-colors cursor-pointer"
      >
        {{ submitting ? 'Creating…' : 'Start screening' }}
      </button>
      <p v-if="error" class="text-sm text-rust-600">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { PatientCreate } from '~/composables/useApi'

const api = useApi()
const router = useRouter()

const form = reactive<PatientCreate>({
  display_id: '',
  age: null,
  sex: null,
  language: 'en',
  facility: '',
  existing_pd_diagnosis: false,
})
const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit() {
  submitting.value = true
  error.value = null
  try {
    const patient = await api.createPatient(form)
    router.push(`/assess/${patient.id}`)
  } catch (e: any) {
    error.value = 'Could not create the patient record. Is the backend running and DATABASE_URL set?'
  } finally {
    submitting.value = false
  }
}
</script>
