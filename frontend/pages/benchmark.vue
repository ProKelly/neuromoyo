<template>
  <main class="min-h-screen bg-paper text-ink">
    <section class="border-b border-mist bg-white">
      <div class="max-w-6xl mx-auto px-5 py-12 sm:py-16">
        <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-8">
          <div class="max-w-3xl">
            <p class="text-xs font-semibold uppercase tracking-[0.18em] text-teal-600 mb-3">NEUROMOYO · Benchmark Evidence</p>
            <h1 class="font-display text-4xl sm:text-5xl font-medium tracking-tight">African code-switched speech, measured.</h1>
            <p class="mt-5 text-lg text-ink-soft leading-relaxed">A reproducible benchmark of four speech recognition systems on the Pidgin test split of AfriSwitch, designed to understand whether African code-switched speech can be converted reliably into downstream clinical information.</p>
          </div>
          <div class="rounded-2xl border border-mist bg-paper px-5 py-4 min-w-[240px]">
            <div class="text-xs uppercase tracking-wide text-ink-soft">Evaluation</div>
            <div class="text-3xl font-semibold mt-1">100 utterances</div>
            <div class="text-sm text-ink-soft mt-1">Seed 20260909 · Pidgin test split</div>
          </div>
        </div>
      </div>
    </section>

    <section class="max-w-6xl mx-auto px-5 py-10 sm:py-14 space-y-10">
      <div class="grid md:grid-cols-4 gap-4">
        <div class="card"><div class="label">Sahara WER</div><div class="metric">{{ pct(best?.mean_WER) }}</div><div class="sub">lowest benchmark WER</div></div>
        <div class="card"><div class="label">Sahara CER</div><div class="metric">{{ pct(best?.mean_CER) }}</div><div class="sub">lowest benchmark CER</div></div>
        <div class="card"><div class="label">Code-switched</div><div class="metric">1,799</div><div class="sub">of 1,801 Pidgin utterances</div></div>
        <div class="card"><div class="label">Systems</div><div class="metric">4</div><div class="sub">Sahara · MMS · Whisper ×2</div></div>
      </div>

      <section class="panel">
        <div class="section-head"><div><p class="eyebrow">Primary result</p><h2>Model comparison</h2></div><span class="badge">Same 100 utterances</span></div>
        <div class="overflow-x-auto">
          <table><thead><tr><th>Model</th><th>Mean WER ↓</th><th>Mean CER ↓</th><th>Latency</th><th>RTF ↓</th></tr></thead>
          <tbody><tr v-for="m in data.models" :key="m.model" :class="m.model === 'Sahara' ? 'winner' : ''"><td class="font-medium">{{ m.model }}</td><td>{{ m.mean_WER.toFixed(3) }}</td><td>{{ m.mean_CER.toFixed(3) }}</td><td>{{ m.mean_latency_s.toFixed(2) }} s</td><td>{{ m.mean_RTF.toFixed(3) }}</td></tr></tbody></table>
        </div>
        <p class="note">WER and CER are transcription metrics; they are not clinical diagnostic accuracy. RTF is real-time factor (lower is faster).</p>
      </section>

      <section class="panel">
        <div class="section-head"><div><p class="eyebrow">Paired uncertainty</p><h2>Sahara versus alternatives</h2></div></div>
        <div class="space-y-4">
          <div v-for="p in data.paired" :key="p.comparison" class="comparison">
            <div><div class="font-medium">{{ p.comparison }}</div><div class="text-sm text-ink-soft">Mean WER difference</div></div>
            <div class="text-right"><div class="font-semibold">{{ p.difference.toFixed(3) }}</div><div class="text-xs text-ink-soft">95% CI [{{ p.low.toFixed(3) }}, {{ p.high.toFixed(3) }}]</div></div>
          </div>
        </div>
      </section>

      <section class="grid lg:grid-cols-2 gap-6">
        <div class="panel"><div class="section-head"><div><p class="eyebrow">Code-mixing intensity</p><h2>CMI robustness</h2></div></div>
          <div v-for="m in data.cmi" :key="m.model" class="slice-row"><span>{{m.model}}</span><span>Low {{m.low.toFixed(2)}} · High {{m.high.toFixed(2)}}</span></div>
          <p class="note">CMI-high/low slices are descriptive robustness analyses within the code-switched Pidgin benchmark.</p>
        </div>
        <div class="panel"><div class="section-head"><div><p class="eyebrow">Switching complexity</p><h2>Switch-point robustness</h2></div></div>
          <div v-for="m in data.switch" :key="m.model" class="slice-row"><span>{{m.model}}</span><span>Low {{m.low.toFixed(2)}} · High {{m.high.toFixed(2)}}</span></div>
          <p class="note">These are WER values for lower versus higher switch-point groups, not a causal estimate of switching effects.</p>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">Methodological boundary</p>
        <h2>Why there is no CS penalty here</h2>
        <p class="mt-4 text-ink-soft leading-relaxed">The full AfriSwitch Pidgin test split contains 1,799 code-switched and only 2 non-code-switched utterances. NEUROMOYO therefore does not manufacture a balanced control group or report a code-switch penalty from two controls. Instead, it analyses variation in CMI, switch-point count and duration inside the code-switched population.</p>
        <div class="mt-5 rounded-xl border border-mist bg-paper p-4 text-sm text-ink-soft">Clinical Information Preservation is a proposed NEUROMOYO downstream metric. It is not an official Intron metric and requires appropriately annotated clinical-domain data.</div>
      </section>

      <footer class="text-sm text-ink-soft pb-8">Dataset: Intron Health AfriSwitch · Pidgin · test split. Evaluation results are reproducible from the NEUROMOYO benchmark notebook. No raw health-related audio is published on this page.</footer>
    </section>
  </main>
</template>

<script setup lang="ts">
type Model = { model: string; n: number; mean_WER: number; mean_CER: number; mean_latency_s: number; mean_RTF: number }
const fallback = { models: [] as Model[], paired: [], cmi: [], switch: [], dataset: {} }
const { data: loaded } = await useFetch('/benchmark.json')
const data = computed(() => loaded.value || fallback)
const best = computed(() => data.value.models.find((m: Model) => m.model === 'Sahara'))
function pct(v?: number) { return v == null ? '—' : `${(v * 100).toFixed(1)}%` }
</script>

<style scoped>
.card,.panel{background:white;border:1px solid #e4ebe8;border-radius:1rem;padding:1.25rem}.card{min-height:128px}.label,.eyebrow{font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;font-weight:700;color:#5f706a}.metric{font-size:2rem;font-weight:700;margin-top:.35rem}.sub,.note{font-size:.78rem;color:#6d7b77;margin-top:.3rem}.section-head{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:1.25rem}.section-head h2{font-family:inherit;font-size:1.45rem;font-weight:600;margin-top:.25rem}.badge{font-size:.72rem;border:1px solid #dce6e2;border-radius:999px;padding:.45rem .7rem;color:#5f706a}.winner{background:#f0f8f4}.comparison,.slice-row{display:flex;justify-content:space-between;gap:1rem;align-items:center;border:1px solid #e7eeeb;border-radius:.8rem;padding:.8rem 1rem}.slice-row{margin-bottom:.55rem;font-size:.86rem}.slice-row span:last-child{color:#66756f;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem}table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:.8rem;border-bottom:1px solid #e7eeeb;white-space:nowrap}th{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:#6d7b77}
</style>
