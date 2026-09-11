<template>
  <div class="min-h-screen flex flex-col">
    <BackgroundPattern />
    <header class="sticky top-0 z-30 print:hidden">
      <div class="border-b border-white/60 bg-paper/90 backdrop-blur-xl shadow-[0_12px_40px_rgba(20,37,32,0.06)]">
        <div class="max-w-6xl mx-auto px-4 sm:px-5 h-16 flex items-center justify-between gap-3">
          <NuxtLink to="/" class="shrink-0 transition-transform duration-200 hover:-translate-y-0.5" @click="mobileOpen = false">
            <Logo size="sm" />
          </NuxtLink>

          <!-- Desktop nav (lg and up) -->
          <nav class="hidden lg:flex items-center gap-2 text-sm">
            <NuxtLink
              v-for="item in publicLinks"
              :key="item.to"
              :to="item.to"
              class="nav-pill"
              :class="isActive(item.to) ? 'nav-pill-active' : 'nav-pill-inactive'"
            >
              {{ t(item.labelKey) }}
            </NuxtLink>
          </nav>

          <div class="hidden lg:flex items-center gap-2 text-sm">
            <template v-if="user">
              <NuxtLink
                class="nav-pill nav-pill-inactive"
                :class="isActive('/') ? 'nav-pill-active' : ''"
                to="/"
              >
                {{ t('nav.dashboard') }}
              </NuxtLink>
              <NuxtLink
                v-if="me && me.role !== 'clinician'"
                class="nav-pill nav-pill-inactive"
                :class="isActive('/team') ? 'nav-pill-active' : ''"
                to="/team"
              >
                {{ t('nav.team') }}
              </NuxtLink>
              <span class="hidden xl:inline text-ink-soft/80 max-w-[12rem] truncate">{{ user.email }}</span>
              <button
                @click="onSignOut"
                class="nav-pill nav-pill-danger"
              >
                {{ t('nav.signOut') }}
              </button>
            </template>
            <NuxtLink v-else to="/login" class="nav-pill nav-pill-primary">
              {{ t('nav.signIn') }}
            </NuxtLink>
            <LanguageToggle />
          </div>

          <!-- Mobile / tablet controls (below lg) -->
          <div class="flex items-center gap-2 lg:hidden">
            <LanguageToggle />
            <button
              type="button"
              class="menu-toggle"
              :aria-expanded="mobileOpen"
              aria-label="Toggle navigation menu"
              @click="mobileOpen = !mobileOpen"
            >
              <svg v-if="!mobileOpen" viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M4 7h16M4 12h16M4 17h16" />
              </svg>
              <svg v-else viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M6 6l12 12M18 6L6 18" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Mobile menu panel -->
        <Transition name="menu-fade">
          <div v-if="mobileOpen" class="lg:hidden border-t border-mist bg-paper/98">
            <nav class="max-w-6xl mx-auto px-4 sm:px-5 py-4 flex flex-col gap-1.5">
              <NuxtLink
                v-for="item in publicLinks"
                :key="item.to"
                :to="item.to"
                class="nav-pill-mobile"
                :class="isActive(item.to) ? 'nav-pill-active' : 'nav-pill-inactive'"
                @click="mobileOpen = false"
              >
                {{ t(item.labelKey) }}
              </NuxtLink>

              <template v-if="user">
                <div class="h-px bg-mist my-2"></div>
                <NuxtLink
                  class="nav-pill-mobile"
                  :class="isActive('/') ? 'nav-pill-active' : 'nav-pill-inactive'"
                  to="/"
                  @click="mobileOpen = false"
                >
                  {{ t('nav.dashboard') }}
                </NuxtLink>
                <NuxtLink
                  v-if="me && me.role !== 'clinician'"
                  class="nav-pill-mobile"
                  :class="isActive('/team') ? 'nav-pill-active' : 'nav-pill-inactive'"
                  to="/team"
                  @click="mobileOpen = false"
                >
                  {{ t('nav.team') }}
                </NuxtLink>
                <p class="text-xs text-ink-soft px-4 pt-2 truncate">{{ user.email }}</p>
                <button class="nav-pill-mobile nav-pill-danger text-left" @click="onSignOut">
                  {{ t('nav.signOut') }}
                </button>
              </template>
              <NuxtLink v-else class="nav-pill-mobile nav-pill-primary" to="/login" @click="mobileOpen = false">
                {{ t('nav.signIn') }}
              </NuxtLink>
            </nav>
          </div>
        </Transition>
      </div>
    </header>
    <main class="flex-1">
      <div :class="isFullWidth ? 'w-full' : 'max-w-3xl mx-auto px-4 sm:px-5 py-6 sm:py-8 w-full'">
        <NuxtPage />
      </div>
    </main>
    <footer class="border-t border-mist py-4 print:hidden bg-paper/80 backdrop-blur-sm">
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
const route = useRoute()
const api = useApi()

type NavItem = { to: string; labelKey: string }

const publicLinks: NavItem[] = [
  { to: '/benchmark', labelKey: 'nav.benchmark' },
  { to: '/about', labelKey: 'nav.about' },
]

initLocale()

// The public landing page manages its own full-bleed section widths (each
// section picks its own inner max-width); every console page stays inside the
// standard max-w-3xl column.
const isFullWidth = computed(() => route.path === '/welcome' || route.path === '/benchmark' || route.path === '/about')

function isActive(to: string) {
  return route.path === to
}

const me = ref<ClinicianMe | null>(null)
watch(user, async (u) => {
  me.value = u ? await api.getMe().catch(() => null) : null
}, { immediate: true })

// The mobile nav panel toggles open/closed independently of screen size so it
// doesn't linger open if the viewport is resized past the `lg` breakpoint,
// and it always closes on navigation (link clicks call this too, but a watch
// covers back/forward navigation and programmatic redirects like sign-out).
const mobileOpen = ref(false)
watch(() => route.fullPath, () => { mobileOpen.value = false })

async function onSignOut() {
  mobileOpen.value = false
  await signOut()
  router.push('/login')
}
</script>

<style scoped>
.nav-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 0.65rem 1rem;
  font-weight: 600;
  transition: all 180ms ease;
  white-space: nowrap;
}

.nav-pill-mobile {
  display: flex;
  align-items: center;
  border-radius: 0.85rem;
  padding: 0.8rem 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 180ms ease;
  width: 100%;
}

.nav-pill-inactive {
  color: var(--color-ink-soft);
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(230, 237, 233, 0.9);
}

.nav-pill-inactive:hover {
  color: var(--color-teal-600);
  border-color: rgba(14, 107, 92, 0.24);
  background: white;
}

.nav-pill-active {
  color: white;
  background: var(--color-teal-600);
  border-color: transparent;
  box-shadow: 0 10px 28px rgba(14, 107, 92, 0.2);
}

.nav-pill-primary {
  color: white;
  background: var(--color-teal-600);
  border: 1px solid transparent;
  box-shadow: 0 10px 28px rgba(14, 107, 92, 0.2);
}

.nav-pill-primary:hover {
  background: var(--color-teal-700);
  transform: translateY(-1px);
}

.nav-pill-danger {
  color: var(--color-rust-700);
  background: var(--color-rust-100);
  border: 1px solid rgba(179, 68, 43, 0.12);
  cursor: pointer;
}

.nav-pill-danger:hover {
  color: white;
  background: var(--color-rust-600);
  border-color: var(--color-rust-600);
}

.menu-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  flex-shrink: 0;
  border-radius: 0.75rem;
  border: 1px solid rgba(230, 237, 233, 0.9);
  background: rgba(255, 255, 255, 0.7);
  color: var(--color-ink-soft);
  cursor: pointer;
  transition: all 180ms ease;
}

.menu-toggle:hover {
  color: var(--color-teal-600);
  border-color: rgba(14, 107, 92, 0.24);
  background: white;
}

.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: opacity 160ms ease, transform 160ms ease;
}
.menu-fade-enter-from,
.menu-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (prefers-reduced-motion: reduce) {
  .menu-fade-enter-active,
  .menu-fade-leave-active {
    transition: none;
  }
}
</style>
