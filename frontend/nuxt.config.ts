import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2026-08-01',
  devtools: { enabled: true },

  // Internal clinician console, not a public site -- no SEO need, and disabling
  // SSR avoids hydration/auth-flicker issues with the Supabase client SDK (which
  // only runs in the browser; see plugins/supabase.client.ts).
  ssr: false,

  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
  },

  runtimeConfig: {
    public: {
      // Points at the FastAPI backend. Override with NUXT_PUBLIC_API_BASE in
      // production (e.g. your Render/Fly/Railway URL); defaults to local dev.
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000',
      supabaseUrl: process.env.NUXT_PUBLIC_SUPABASE_URL || '',
      supabaseAnonKey: process.env.NUXT_PUBLIC_SUPABASE_ANON_KEY || '',
    },
  },

  app: {
    head: {
      title: 'Neuromoyo — NeuroVoice',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'AI-assisted voice screening for Parkinsonian speech patterns.' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
    },
  },
})
