<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b border-mist bg-white sticky top-0 z-10 print:hidden">
      <div class="max-w-3xl mx-auto px-4 sm:px-5 py-3.5 flex items-center justify-between gap-3">
        <NuxtLink to="/" class="shrink-0">
          <Logo size="sm" />
        </NuxtLink>
        <div v-if="user" class="flex items-center gap-3 sm:gap-4 text-sm">
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
    <main class="flex-1">
      <div class="max-w-3xl mx-auto px-4 sm:px-5 py-6 sm:py-8 w-full">
        <NuxtPage />
      </div>
    </main>
    <footer class="border-t border-mist py-4 print:hidden">
      <p class="max-w-3xl mx-auto px-4 sm:px-5 text-xs text-ink-soft">
        {{ t('footer.disclaimer') }}
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
const { user, signOut } = useAuth()
const { t, initLocale } = useI18n()
const router = useRouter()

initLocale()

async function onSignOut() {
  await signOut()
  router.push('/login')
}
</script>
