<template>
  <section class="bg-white border border-mist rounded-2xl p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="font-display text-xl font-medium text-ink">{{ t('assess.nav.details') }}</h2>
      <button
        v-if="!editing" @click="startEdit"
        class="text-sm font-medium text-teal-600 hover:text-teal-700 cursor-pointer"
      >
        Edit
      </button>
    </div>

    <dl v-if="!editing && patient" class="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
      <dt class="text-ink-soft">Patient ID</dt><dd class="text-ink font-medium">{{ patient.display_id }}</dd>
      <dt class="text-ink-soft">Age</dt><dd class="text-ink">{{ patient.age ?? '—' }}</dd>
      <dt class="text-ink-soft">Sex</dt><dd class="text-ink capitalize">{{ patient.sex || '—' }}</dd>
      <dt class="text-ink-soft">Language</dt><dd class="text-ink">{{ (patient.language || 'en').toUpperCase() }}</dd>
      <dt class="text-ink-soft">Facility</dt><dd class="text-ink">{{ patient.facility || '—' }}</dd>
      <dt class="text-ink-soft">Existing PD diagnosis</dt><dd class="text-ink">{{ patient.existing_pd_diagnosis ? 'Yes' : 'No' }}</dd>
      <dt class="text-ink-soft">On PD medication</dt><dd class="text-ink">{{ patient.on_pd_medication ? 'Yes' : 'No' }}</dd>
    </dl>

    <form v-else class="flex flex-col gap-4" @submit.prevent="saveEdit">
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Patient ID</span>
        <input v-model="editForm.display_id" required class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600" />
      </label>
      <div class="grid grid-cols-2 gap-4">
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Age</span>
          <input v-model.number="editForm.age" type="number" min="0" max="120" class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600" />
        </label>
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Sex</span>
          <select v-model="editForm.sex" class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600">
            <option :value="null">Prefer not to say</option>
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>
        </label>
      </div>
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Language</span>
        <select v-model="editForm.language" class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600">
          <option value="en">English</option>
          <option value="fr">Français</option>
        </select>
      </label>
      <label v-if="isAdmin" class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">Facility (admin only)</span>
        <input v-model="editForm.facility" class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600" />
      </label>
      <label class="flex items-center gap-2.5">
        <input v-model="editForm.existing_pd_diagnosis" type="checkbox" class="w-4 h-4 rounded border-mist text-teal-600 focus:ring-teal-600" />
        <span class="text-sm text-ink-soft">Existing Parkinson's diagnosis</span>
      </label>
      <label class="flex items-center gap-2.5">
        <input v-model="editForm.on_pd_medication" type="checkbox" class="w-4 h-4 rounded border-mist text-teal-600 focus:ring-teal-600" />
        <span class="text-sm text-ink-soft">On Parkinson's medication</span>
      </label>

      <div class="flex gap-3">
        <button type="submit" :disabled="editSaving" class="rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 text-white text-sm font-semibold px-5 py-2.5 transition-colors cursor-pointer">
          {{ editSaving ? 'Saving…' : 'Save changes' }}
        </button>
        <button type="button" @click="editing = false" class="rounded-full border border-mist text-sm font-medium text-ink-soft px-5 py-2.5 hover:bg-mist transition-colors cursor-pointer">
          Cancel
        </button>
      </div>
      <p v-if="editError" class="text-sm text-rust-600">{{ editError }}</p>
    </form>
  </section>
</template>

<script setup lang="ts">
import type { ClinicianMe, Patient, PatientUpdate } from '~/composables/useApi'

const patientId = inject<string>('patientId')!
const patient = inject<Ref<Patient | null>>('patient')!
const me = inject<Ref<ClinicianMe | null>>('me')!
const refetchPatient = inject<() => Promise<void>>('refetchPatient')!
const api = useApi()
const { t } = useI18n()

const isAdmin = computed(() => me.value?.role === 'admin')

const editing = ref(false)
const editForm = ref<PatientUpdate>({})
const editSaving = ref(false)
const editError = ref<string | null>(null)

function startEdit() {
  if (!patient.value) return
  editForm.value = {
    display_id: patient.value.display_id,
    age: patient.value.age,
    sex: patient.value.sex,
    language: patient.value.language,
    facility: patient.value.facility,
    existing_pd_diagnosis: patient.value.existing_pd_diagnosis,
    on_pd_medication: patient.value.on_pd_medication,
  }
  editError.value = null
  editing.value = true
}

async function saveEdit() {
  editSaving.value = true
  editError.value = null
  try {
    await api.updatePatient(patientId, editForm.value)
    await refetchPatient()
    editing.value = false
  } catch (e: any) {
    editError.value = e?.data?.detail || 'Could not save changes.'
  } finally {
    editSaving.value = false
  }
}
</script>
