<template>
  <div class="max-w-sm mx-auto mt-6 sm:mt-10 px-1">
    <div class="mb-6 flex justify-center">
      <Logo size="lg" :show-tagline="false" />
    </div>
    <h1 class="font-display text-2xl font-medium text-ink mb-1 text-center">{{ t('login.title') }}</h1>
    <p class="text-ink-soft text-sm mb-6 text-center">{{ t('login.subtitle') }}</p>

    <form class="bg-white border border-mist rounded-2xl p-6 flex flex-col gap-4" @submit.prevent="onSubmit">
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">{{ t('login.email') }}</span>
        <input
          v-model="email" type="email" required autocomplete="username"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
      </label>
      <label class="flex flex-col gap-1.5">
        <span class="text-sm font-medium text-ink-soft">{{ t('login.password') }}</span>
        <input
          v-model="password" type="password" required autocomplete="current-password"
          class="rounded-lg border border-mist px-3.5 py-2.5 text-ink placeholder:text-ink-soft/50 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600"
        />
      </label>
      <button
        type="submit" :disabled="submitting"
        class="mt-1 rounded-full bg-teal-600 hover:bg-teal-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3 transition-colors cursor-pointer"
      >
        {{ submitting ? t('login.submitting') : t('login.submit') }}
      </button>
      <p v-if="error" class="text-sm text-rust-600">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
const { signInWithPassword } = useAuth()
const { t, initLocale } = useI18n()
const router = useRouter()

initLocale()

const email = ref('')
const password = ref('')
const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit() {
  submitting.value = true
  error.value = null
  try {
    await signInWithPassword(email.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e?.message || 'Sign-in failed. Check your email and password.'
  } finally {
    submitting.value = false
  }
}
</script>
