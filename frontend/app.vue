<!-- app.vue -->
<template>
  <div class="min-h-screen flex flex-col relative">
    <!-- Global subtle pattern background -->
    <div class="fixed inset-0 pointer-events-none opacity-[0.015] z-0">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle at 30% 40%, #0d9488 1px, transparent 1px); background-size: 32px 32px;"></div>
    </div>
    
    <!-- Decorative corner blobs -->
    <div class="fixed top-0 right-0 w-96 h-96 pointer-events-none opacity-[0.02] z-0">
      <div class="absolute inset-0" style="background: radial-gradient(circle at 100% 0%, #0d9488, transparent 70%);"></div>
    </div>
    <div class="fixed bottom-0 left-0 w-96 h-96 pointer-events-none opacity-[0.02] z-0">
      <div class="absolute inset-0" style="background: radial-gradient(circle at 0% 100%, #0d9488, transparent 70%);"></div>
    </div>

    <header class="border-b border-mist bg-white/80 backdrop-blur-sm sticky top-0 z-10 print:hidden relative">
      <div class="max-w-3xl mx-auto px-4 sm:px-5 py-3.5 flex items-center justify-between gap-3">
        <NuxtLink to="/" class="shrink-0">
          <Logo size="sm" />
        </NuxtLink>
        <div v-if="user" class="flex items-center gap-3 sm:gap-4 text-sm">
          <NuxtLink
            v-if="me && me.role !== 'clinician'" to="/team"
            class="text-ink-soft hover:text-teal-600 font-medium transition-colors whitespace-nowrap"
          >
            {{ t('nav.team') }}
          </NuxtLink>
          <span class="text-ink-soft hidden sm:inline truncate max-w-[14rem]">{{ user.email }}</span>
          <button
            @click="onSignOut"
            class="text-ink-soft hover:text-rust-600 font-medium cursor-pointer transition-colors whitespace-nowrap"
          >
            {{ t('nav.signOut') }}
          </button>
        </div>
      </div>
    </header>
    <main class="flex-1 relative z-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-5 py-6 sm:py-8 w-full">
        <NuxtPage />
      </div>
    </main>
    <footer class="border-t border-mist py-4 print:hidden relative bg-white/50 backdrop-blur-sm">
      <p class="max-w-3xl mx-auto px-4 sm:px-5 text-xs text-ink-soft">
        {{ t('footer.disclaimer') }}
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import type { ClinicianMe } from '~/composables/useApi'

const { user, signOut } = useAuth()
const { t, initLocale } = useI18n()
const router = useRouter()
const api = useApi()

initLocale()

const me = ref<ClinicianMe | null>(null)
watch(user, async (u) => {
  me.value = u ? await api.getMe().catch(() => null) : null
}, { immediate: true })

async function onSignOut() {
  await signOut()
  router.push('/login')
}
</script>