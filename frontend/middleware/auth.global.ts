// Runs on every navigation. Supabase Auth only exists client-side here (see
// plugins/supabase.client.ts), so this is a no-op during SSR -- the client-side
// run after hydration is what actually gates the page.
export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const { user, ready, init } = useAuth()
  if (!ready.value) await init()

  const isLoginPage = to.path === '/login'
  const isWelcomePage = to.path === '/welcome'
  // Reachable regardless of auth state, and NOT force-redirected away even if
  // `user` is already truthy -- clicking an invite link gives a temporary
  // session (see accept-invite.vue's docblock), and that page needs to run
  // regardless of whether session-from-URL detection has resolved by the time
  // this middleware's own getSession() call does. The page itself shows an
  // "invalid/expired" state if there's genuinely no session.
  const isBenchmarkPage = to.path === '/benchmark'
  const isAcceptInvitePage = to.path === '/accept-invite'
  if (isAcceptInvitePage || isBenchmarkPage) return

  // Signed-in clinicians skip the marketing/login pages and go straight to the console.
  if (user.value && (isLoginPage || isWelcomePage)) {
    return navigateTo('/')
  }
  // Signed-out visitors land on the short welcome page first, not a bare login form.
  if (!user.value && !isLoginPage && !isWelcomePage) {
    return navigateTo('/welcome')
  }
})
