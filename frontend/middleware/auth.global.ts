// Runs on every navigation. Supabase Auth only exists client-side here (see
// plugins/supabase.client.ts), so this is a no-op during SSR -- the client-side
// run after hydration is what actually gates the page.
export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const { user, ready, init } = useAuth()
  if (!ready.value) await init()

  const isLoginPage = to.path === '/login'
  const isWelcomePage = to.path === '/welcome'

  // Signed-in clinicians skip the marketing/login pages and go straight to the console.
  if (user.value && (isLoginPage || isWelcomePage)) {
    return navigateTo('/')
  }
  // Signed-out visitors land on the short welcome page first, not a bare login form.
  if (!user.value && !isLoginPage && !isWelcomePage) {
    return navigateTo('/welcome')
  }
})
