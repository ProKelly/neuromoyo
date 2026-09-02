<!--
  Where a clinician invite email actually lands (see backend's
  app/supabase_admin.py, which sets this as the invite link's redirect_to).
  Clicking the emailed link gives Supabase-js a temporary session, parsed
  automatically from the URL by plugins/supabase.client.ts's
  detectSessionInUrl -- but a temporary session with no password set is a dead
  end, not a login. This page is the missing step: set a real password once,
  and from then on it's a normal account.
-->
<template>
  <div class="max-w-sm mx-auto mt-6 sm:mt-10 px-1">
    <div class="mb-6 flex justify-center">
      <Logo size="lg" :show-tagline="false" />
    </div>

    <div v-if="!ready" class="text-center text-ink-soft text-sm">Loading…</div>

    <div v-else-if="!user" class="bg-white border border-rust-100 rounded-2xl p-6 text-sm text-rust-600">
      This invite link looks invalid or has expired. Ask whoever invited you to send a new one.
    </div>

    <template v-else>
      <h1 class="font-display text-2xl font-medium text-ink mb-1 text-center">Set your password</h1>
      <p class="text-ink-soft text-sm mb-6 text-center">{{ user.email }}</p>

      <form class="bg-white border border-mist rounded-2xl p-6 flex flex-col gap-4" @submit.prevent="onSubmit">
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Password</span>
          <input
            v-model="password" type="password" required minlength="8" autocomplete="new-password"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          />
        </label>
        <label class="flex flex-col gap-1.5">
          <span class="text-sm font-medium text-ink-soft">Confirm password</span>
          <input
            v-model="confirm" type="password" required minlength="8" autocomplete="new-password"
            class="rounded-lg border border-mist px-3.5 py-2.5 text-ink focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
          />
        </label>
        <button
          type="submit" :disabled="submitting"
          class="mt-1 rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3 transition-colors cursor-pointer"
        >
          {{ submitting ? 'Setting password…' : 'Set password and continue' }}
        </button>
        <p v-if="error" class="text-sm text-rust-600">{{ error }}</p>
      </form>
    </template>
  </div>
</template>

<script setup lang="ts">
const { user, ready, init, setPassword } = useAuth()
const router = useRouter()

const password = ref('')
const confirm = ref('')
const submitting = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  if (!ready.value) await init()
})

async function onSubmit() {
  error.value = null
  if (password.value !== confirm.value) {
    error.value = "Passwords don't match."
    return
  }
  submitting.value = true
  try {
    await setPassword(password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e?.message || 'Could not set your password. Try requesting a new invite.'
  } finally {
    submitting.value = false
  }
}
</script>
