<template>
  <div>
    <NuxtLink to="/" class="text-sm text-teal-600 hover:text-teal-700 font-medium mb-4 inline-block">
      ← {{ t('assess.backToDashboard') }}
    </NuxtLink>
    <p class="text-xs font-semibold tracking-wide uppercase text-teal-600 mb-2">{{ t('intake.step') }}</p>
    <h1 class="font-display text-3xl font-medium text-ink mb-1">{{ t('intake.title') }}</h1>
    <p class="text-ink-soft mb-8">{{ t('intake.subtitle') }}</p>

    <form class="bg-white border border-mist rounded-2xl p-5 sm:p-6 flex flex-col gap-5" @submit.prevent="onSubmit">
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">{{ t('intake.patientId') }}</span>
        <input
          v-model="form.display_id" required placeholder="e.g. BDA-0042"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
      </label>

      <div class="grid grid-cols-2 gap-4">
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">{{ t('intake.age') }}</span>
          <input
            v-model.number="form.age" type="number" min="0" max="120"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          />
        </label>
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">{{ t('intake.sex') }}</span>
          <select
            v-model="form.sex"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          >
            <option :value="null">{{ t('intake.sex.unspecified') }}</option>
            <option value="female">{{ t('intake.sex.female') }}</option>
            <option value="male">{{ t('intake.sex.male') }}</option>
          </select>
        </label>
      </div>

      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">{{ t('intake.language') }}</span>
        <select
          v-model="form.language"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        >
          <option value="en">English</option>
          <option value="fr">Français</option>
        </select>
      </label>

      <!--
        Non-admin clinicians never see a facility field at all: the backend
        assigns it automatically from the clinician's own record on save (see
        routers/patients.py), so there's no free-text field to typo in the
        first place. Admins aren't tied to one facility, so they still need to
        pick one -- but from a list of facilities already in use, not a blank
        text box, so it's still typo-proof.
      -->
      <div v-if="isAdmin" class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">{{ t('intake.facility') }}</span>
        <input
          v-model="form.facility" required list="facility-options" placeholder="Clinic / hospital name"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
        <datalist id="facility-options">
          <option v-for="f in facilities" :key="f" :value="f" />
        </datalist>
      </div>
      <p v-else-if="me" class="text-sm text-ink-soft">
        {{ t('intake.facility') }}: <span class="font-medium text-ink">{{ me.facility || '—' }}</span>
      </p>

      <label class="flex items-center gap-2.5">
        <input v-model="form.existing_pd_diagnosis" type="checkbox" class="w-4 h-4 rounded border-mist text-teal-600 focus:ring-teal-600" />
        <span class="text-sm text-ink-soft">{{ t('intake.existingDx') }}</span>
      </label>

      <button
        type="submit" :disabled="submitting"
        class="mt-1 rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3 transition-colors cursor-pointer"
      >
        {{ submitting ? t('intake.submitting') : t('intake.submit') }}
      </button>
      <p v-if="error" class="text-sm text-rust-600">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { ClinicianMe, PatientCreate } from '~/composables/useApi'

const api = useApi()
const router = useRouter()
const { t } = useI18n()

const me = ref<ClinicianMe | null>(null)
const facilities = ref<string[]>([])
const isAdmin = computed(() => me.value?.role === 'admin')

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

onMounted(async () => {
  me.value = await api.getMe()
  if (me.value.role === 'admin') facilities.value = await api.listFacilities()
})

async function onSubmit() {
  submitting.value = true
  error.value = null
  try {
    // Non-admins: don't send `facility` at all -- the server assigns it from
    // the clinician's own record, so there's nothing here for a client-side
    // typo (or a tampered request) to override.
    const payload = isAdmin.value ? form : { ...form, facility: undefined }
    const patient = await api.createPatient(payload)
    router.push(`/assess/${patient.id}`)
  } catch (e: any) {
    error.value = e?.data?.detail || "Could not create the patient record. Is the backend running and DATABASE_URL set?"
  } finally {
    submitting.value = false
  }
}
</script>
