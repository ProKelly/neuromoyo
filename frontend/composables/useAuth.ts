// Thin reactive wrapper around Supabase Auth. `user`/`ready` are shared app-wide
// via useState so the header, route middleware, and login page all see the same
// session without each re-deriving it.
export interface AuthUser {
  id: string
  email: string | null
}

export function useAuth() {
  const { $supabase } = useNuxtApp()
  const user = useState<AuthUser | null>('auth:user', () => null)
  const ready = useState<boolean>('auth:ready', () => false)
  const started = useState<boolean>('auth:started', () => false)

  function toAuthUser(supaUser: { id: string; email?: string | null } | null | undefined): AuthUser | null {
    return supaUser ? { id: supaUser.id, email: supaUser.email ?? null } : null
  }

  async function init() {
    if (started.value) return
    started.value = true
    const { data } = await $supabase.auth.getSession()
    user.value = toAuthUser(data.session?.user)
    ready.value = true
    $supabase.auth.onAuthStateChange((_event: string, session: { user: any } | null) => {
      user.value = toAuthUser(session?.user)
    })
  }

  async function signInWithPassword(email: string, password: string) {
    const { error } = await $supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
  }

  async function setPassword(password: string) {
    // Used by accept-invite.vue: at this point the person has a temporary
    // session from clicking their invite link (Supabase parsed it from the URL
    // automatically -- see plugins/supabase.client.ts's detectSessionInUrl).
    // This turns that temporary session into a real account they can log back
    // into later with email + this password.
    const { error } = await $supabase.auth.updateUser({ password })
    if (error) throw error
  }

  async function signOut() {
    await $supabase.auth.signOut()
    user.value = null
  }

  async function getAccessToken(): Promise<string | null> {
    const { data } = await $supabase.auth.getSession()
    return data.session?.access_token ?? null
  }

  return { user, ready, init, signInWithPassword, setPassword, signOut, getAccessToken }
}
