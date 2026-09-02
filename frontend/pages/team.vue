<!--
  The production onboarding console: a global admin registers facilities and
  invites each one's first facility_admin; a facility_admin invites their own
  facility's clinicians. Deliberately gated, not self-serve -- see Facility's
  docstring in backend/app/models.py. Invisible to a plain "clinician" (guarded
  both by the nav link in app.vue and by a redirect here).
-->
<template>
  <div v-if="me && me.role !== 'clinician'">
    <h1 class="font-display text-3xl font-medium text-ink mb-1">{{ t('team.title') }}</h1>
    <p class="text-ink-soft mb-6">
      {{ isAdmin ? t('team.subtitle.admin') : t('team.subtitle.facilityAdmin') }}
    </p>

    <!-- Facility registration: global admin only -->
    <section v-if="isAdmin" class="bg-white border border-mist rounded-2xl p-5 sm:p-6 mb-6">
      <h2 class="font-display text-lg font-medium text-ink mb-3">{{ t('team.facilities') }}</h2>

      <ul v-if="facilities.length" class="divide-y divide-mist mb-5 text-sm">
        <li v-for="f in facilities" :key="f.id" class="py-2 text-ink">{{ f.name }}</li>
      </ul>
      <p v-else class="text-sm text-ink-soft mb-5">{{ t('team.noFacilities') }}</p>

      <form class="flex flex-col sm:flex-row gap-3" @submit.prevent="onCreateFacility">
        <input
          v-model="newFacilityName" required :placeholder="t('team.facilityName')"
          class="flex-1 rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600"
        />
        <button
          type="submit" :disabled="creatingFacility"
          class="rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 text-white text-sm font-semibold px-5 py-2.5 transition-colors cursor-pointer whitespace-nowrap"
        >
          {{ t('team.createFacility') }}
        </button>
      </form>
      <p v-if="facilityError" class="text-sm text-rust-600 mt-2">{{ facilityError }}</p>
    </section>

    <!-- Invite -->
    <section class="bg-white border border-mist rounded-2xl p-5 sm:p-6 mb-6">
      <h2 class="font-display text-lg font-medium text-ink mb-3">
        {{ isAdmin ? t('team.inviteFacilityAdmin') : t('team.inviteClinician') }}
      </h2>
      <form class="flex flex-col gap-4" @submit.prevent="onInvite">
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">{{ t('team.email') }}</span>
          <input
            v-model="inviteEmail" type="email" required
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600"
          />
        </label>

        <label v-if="isAdmin" class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">{{ t('team.facility') }}</span>
          <select
            v-model="inviteFacilityId" required
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600"
          >
            <option value="" disabled>—</option>
            <option v-for="f in facilities" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </label>
        <p v-else class="text-sm text-ink-soft">{{ t('team.facility') }}: <span class="text-ink font-medium">{{ me.facility }}</span></p>

        <label v-if="isAdmin" class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">{{ t('team.role') }}</span>
          <select
            v-model="inviteRole"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink bg-white focus:outline-none focus:ring-2 focus:ring-teal-600"
          >
            <option value="facility_admin">{{ t('team.role.facility_admin') }}</option>
            <option value="clinician">{{ t('team.role.clinician') }}</option>
          </select>
        </label>

        <button
          type="submit" :disabled="inviting"
          class="self-start rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 text-white text-sm font-semibold px-5 py-2.5 transition-colors cursor-pointer"
        >
          {{ inviting ? t('team.inviting') : t('team.invite') }}
        </button>
        <p v-if="inviteSuccess" class="text-sm text-teal-600">{{ t('team.inviteSent') }}</p>
        <p v-if="inviteError" class="text-sm text-rust-600">{{ inviteError }}</p>
      </form>
    </section>

    <!-- Roster -->
    <section class="bg-white border border-mist rounded-2xl p-5 sm:p-6">
      <h2 class="font-display text-lg font-medium text-ink mb-3">{{ t('team.roster') }}</h2>
      <p v-if="clinicians.length === 0" class="text-sm text-ink-soft">{{ t('team.noClinicians') }}</p>
      <ul v-else class="divide-y divide-mist text-sm">
        <li v-for="c in clinicians" :key="c.id" class="py-2.5 flex items-center justify-between gap-3">
          <div class="min-w-0">
            <span class="text-ink font-medium">{{ c.email }}</span>
            <span v-if="isAdmin && c.facility" class="text-ink-soft ml-2">· {{ c.facility }}</span>
          </div>
          <span class="text-xs font-mono text-ink-soft shrink-0">{{ t(`team.role.${c.role}`) || c.role }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { ClinicianMe, Facility } from '~/composables/useApi'

const api = useApi()
const { t } = useI18n()

const me = ref<ClinicianMe | null>(null)
const isAdmin = computed(() => me.value?.role === 'admin')

const facilities = ref<Facility[]>([])
const clinicians = ref<ClinicianMe[]>([])

const newFacilityName = ref('')
const creatingFacility = ref(false)
const facilityError = ref<string | null>(null)

const inviteEmail = ref('')
const inviteFacilityId = ref('')
const inviteRole = ref<'clinician' | 'facility_admin'>('facility_admin')
const inviting = ref(false)
const inviteError = ref<string | null>(null)
const inviteSuccess = ref(false)

onMounted(async () => {
  me.value = await api.getMe()
  if (me.value.role === 'clinician') return // guarded again in the template; nothing more to load
  const tasks: Promise<any>[] = [api.listClinicians()]
  if (me.value.role === 'admin') tasks.push(api.listFacilities())
  const results = await Promise.all(tasks)
  clinicians.value = results[0]
  if (me.value.role === 'admin') facilities.value = results[1]
})

async function onCreateFacility() {
  creatingFacility.value = true
  facilityError.value = null
  try {
    const f = await api.createFacility(newFacilityName.value)
    facilities.value.push(f)
    facilities.value.sort((a, b) => a.name.localeCompare(b.name))
    newFacilityName.value = ''
  } catch (e: any) {
    facilityError.value = e?.data?.detail || 'Could not create facility.'
  } finally {
    creatingFacility.value = false
  }
}

async function onInvite() {
  inviting.value = true
  inviteError.value = null
  inviteSuccess.value = false
  try {
    const facilityId = isAdmin.value ? inviteFacilityId.value : me.value!.facility_id!
    const role = isAdmin.value ? inviteRole.value : 'clinician'
    const newClinician = await api.inviteClinician({ email: inviteEmail.value, facility_id: facilityId, role })
    clinicians.value.push(newClinician)
    inviteEmail.value = ''
    inviteSuccess.value = true
  } catch (e: any) {
    inviteError.value = e?.data?.detail || 'Could not send invite.'
  } finally {
    inviting.value = false
  }
}
</script>
