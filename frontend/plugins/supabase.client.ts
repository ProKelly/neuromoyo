// Client-only: Supabase Auth (session, tokens) is a browser concern here -- the
// console is a connected clinician web app (per the README), not SSR'd per-user.
import { createClient } from '@supabase/supabase-js'

export default defineNuxtPlugin(() => {
  const { public: { supabaseUrl, supabaseAnonKey } } = useRuntimeConfig()

  if (!supabaseUrl || !supabaseAnonKey) {
    console.warn(
      'NUXT_PUBLIC_SUPABASE_URL / NUXT_PUBLIC_SUPABASE_ANON_KEY are not set -- ' +
      'copy frontend/.env.example to frontend/.env and fill them in, or login will fail.'
    )
  }

  const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
    },
  })

  return {
    provide: { supabase },
  }
})
