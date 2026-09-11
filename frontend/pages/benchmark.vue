<template>
  <main class="min-h-screen bg-paper text-ink">
    <!-- Hero -->
    <section class="border-b border-mist bg-white">
      <div class="max-w-7xl mx-auto px-5 py-12 sm:py-16">
        <div class="grid lg:grid-cols-[1fr_auto] gap-8 items-end">
          <div class="max-w-4xl">
            <p class="eyebrow text-teal-600">NEUROMOYO · Benchmark evidence</p>
            <h1 class="font-display text-4xl sm:text-5xl lg:text-6xl font-medium tracking-tight leading-[1.05] mt-3">
              Can African code-switched speech be understood reliably?
            </h1>
            <p class="mt-5 text-lg sm:text-xl text-ink-soft leading-relaxed max-w-3xl">
              We compared four speech recognition systems on the same 100 Pidgin utterances from the
              <strong>AfriSwitch</strong> test split. The goal is simple: find the speech layer that best
              preserves what a patient actually said for downstream clinical use.
            </p>
            <div class="mt-6 flex flex-wrap gap-2">
              <span class="pill">Pidgin · test split</span>
              <span class="pill">100 utterances</span>
              <span class="pill">4 ASR systems</span>
              <span class="pill">Same evaluation set</span>
            </div>
          </div>

          <div class="hero-stat">
            <div class="label">Best mean WER</div>
            <div class="hero-number">{{ pct(best?.mean_WER) }}</div>
            <div class="font-semibold">Sahara</div>
            <div class="text-sm text-ink-soft mt-1">Lower is better</div>
          </div>
        </div>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-5 py-10 sm:py-14 space-y-8">
      <!-- Executive summary -->
      <section class="grid md:grid-cols-4 gap-4">
        <div class="card accent">
          <div class="label">Sahara WER</div>
          <div class="metric">{{ pct(best?.mean_WER) }}</div>
          <div class="sub">lowest mean word error rate</div>
        </div>
        <div class="card">
          <div class="label">Sahara CER</div>
          <div class="metric">{{ pct(best?.mean_CER) }}</div>
          <div class="sub">lowest mean character error rate</div>
        </div>
        <div class="card">
          <div class="label">MMS-1B RTF</div>
          <div class="metric">{{ bestSpeed ? bestSpeed.mean_RTF.toFixed(3) : '—' }}</div>
          <div class="sub">fastest real-time factor</div>
        </div>
        <div class="card">
          <div class="label">Benchmark coverage</div>
          <div class="metric">1,801</div>
          <div class="sub">total Pidgin test utterances in source split</div>
        </div>
      </section>

      <!-- Plain-English takeaway -->
      <section class="takeaway">
        <div class="takeaway-icon">01</div>
        <div>
          <p class="eyebrow">The result in plain English</p>
          <h2 class="mt-1">Sahara made the fewest transcription errors in this evaluation.</h2>
          <p class="mt-3 text-ink-soft leading-relaxed">
            Sahara had the lowest mean WER and CER. MMS-1B was substantially faster by real-time factor.
            So the engineering trade-off is clear: <strong>accuracy favours Sahara in this test; speed favours MMS-1B.</strong>
          </p>
        </div>
      </section>

      <!-- Visual WER chart -->
      <section class="panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">1 · Accuracy</p>
            <h2>Word error rate — lower is better</h2>
            <p class="section-copy">WER estimates how often words in the reference transcription are incorrectly recognised.</p>
          </div>
          <span class="badge">Mean WER</span>
        </div>

        <div class="chart-wrap">
          <div v-for="m in data.models" :key="`wer-${m.model}`" class="bar-row">
            <div class="bar-label">
              <span class="font-semibold">{{ m.model }}</span>
              <span class="bar-value">{{ m.mean_WER.toFixed(3) }}</span>
            </div>
            <div class="bar-track">
              <div
                class="bar-fill"
                :class="{ best: m.model === 'Sahara' }"
                :style="{ width: `${barWidth(m.mean_WER, maxWER)}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="callout">
          <span class="dot"></span>
          <span><strong>Sahara:</strong> 0.526 mean WER. Its mean WER is about {{ improvementVsMMS }}% lower than MMS-1B in this benchmark.</span>
        </div>
      </section>

      <!-- Visual RTF chart -->
      <section class="panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">2 · Speed</p>
            <h2>Real-time factor — lower is faster</h2>
            <p class="section-copy">
              RTF is processing time divided by audio duration. An RTF of 0.10 means roughly 1 second
              of processing per 10 seconds of audio on the benchmark setup.
            </p>
          </div>
          <span class="badge">Mean RTF</span>
        </div>

        <div class="chart-wrap">
          <div v-for="m in data.models" :key="`rtf-${m.model}`" class="bar-row">
            <div class="bar-label">
              <span class="font-semibold">{{ m.model }}</span>
              <span class="bar-value">{{ m.mean_RTF.toFixed(3) }}</span>
            </div>
            <div class="bar-track">
              <div
                class="bar-fill speed"
                :class="{ best: m.model === bestSpeed?.model }"
                :style="{ width: `${barWidth(m.mean_RTF, maxRTF)}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="callout neutral">
          <span class="dot"></span>
          <span><strong>MMS-1B:</strong> fastest in this benchmark at 0.047 RTF. Speed and transcription accuracy should therefore be considered together.</span>
        </div>
      </section>

      <!-- Comparison table -->
      <section class="panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">3 · Full comparison</p>
            <h2>What each system delivered</h2>
            <p class="section-copy">All four systems were evaluated on the same 100 utterances.</p>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table>
            <thead>
              <tr>
                <th>System</th>
                <th>Mean WER ↓</th>
                <th>Mean CER ↓</th>
                <th>Median WER ↓</th>
                <th>Latency</th>
                <th>RTF ↓</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in data.models" :key="m.model" :class="{ winner: m.model === 'Sahara' }">
                <td>
                  <div class="flex items-center gap-2">
                    <span v-if="m.model === 'Sahara'" class="winner-mark">Best WER</span>
                    <span class="font-semibold">{{ m.model }}</span>
                  </div>
                </td>
                <td class="numeric">{{ m.mean_WER.toFixed(3) }}</td>
                <td class="numeric">{{ m.mean_CER.toFixed(3) }}</td>
                <td class="numeric">{{ medianWER(m) }}</td>
                <td class="numeric">{{ m.mean_latency_s.toFixed(2) }} s</td>
                <td class="numeric">{{ m.mean_RTF.toFixed(3) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="legend-row">
          <span><strong>WER</strong> = word error rate</span>
          <span><strong>CER</strong> = character error rate</span>
          <span><strong>RTF</strong> = real-time factor</span>
        </div>
        <p class="note">
          These are ASR metrics, not clinical diagnostic accuracy. Lower is better for WER, CER, latency and RTF.
        </p>
      </section>

      <!-- Uncertainty -->
      <section class="panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">4 · Statistical confidence</p>
            <h2>Was Sahara's advantage consistent?</h2>
            <p class="section-copy">
              Paired bootstrap intervals show the distribution of Sahara's WER difference against each alternative.
              More negative values favour Sahara.
            </p>
          </div>
        </div>

        <div class="interval-chart">
          <div class="zero-line" :style="{ left: `${intervalPosition(0)}%` }"></div>
          <div v-for="p in data.paired" :key="p.comparison" class="interval-row">
            <div class="interval-label">{{ shortComparison(p.comparison) }}</div>
            <div class="interval-track">
              <div
                class="interval"
                :style="{
                  left: `${intervalPosition(p.low)}%`,
                  width: `${Math.max(1, intervalPosition(p.high) - intervalPosition(p.low))}%`
                }"
              ></div>
              <span class="interval-point" :style="{ left: `${intervalPosition(p.difference)}%` }"></span>
            </div>
            <div class="interval-value">{{ signed(p.difference) }}</div>
          </div>
          <div class="interval-axis">
            <span>-3.5</span><span>-2.5</span><span>-1.5</span><span>-0.5</span><span>0</span>
          </div>
        </div>

        <p class="note">
          All reported intervals are paired 95% bootstrap confidence intervals from the frozen benchmark.
          The intervals shown here support the observed pairwise WER differences; they do not establish clinical superiority.
        </p>
      </section>

      <!-- Robustness -->
      <section class="grid lg:grid-cols-2 gap-6">
        <section class="panel">
          <div class="section-head">
            <div>
              <p class="eyebrow">5 · Robustness</p>
              <h2>Does performance change with code-mixing intensity?</h2>
              <p class="section-copy">CMI = Code Mixing Index. Lower WER is better.</p>
            </div>
          </div>

          <div class="mini-chart">
            <div v-for="m in data.cmi" :key="`cmi-${m.model}`" class="mini-row">
              <div class="mini-name">{{ m.model }}</div>
              <div class="mini-bars">
                <div class="mini-track">
                  <span class="mini-caption">Low</span>
                  <div class="mini-fill" :style="{ width: `${miniWidth(m.low)}%` }"></div>
                  <strong>{{ m.low.toFixed(2) }}</strong>
                </div>
                <div class="mini-track">
                  <span class="mini-caption">High</span>
                  <div class="mini-fill high" :style="{ width: `${miniWidth(m.high)}%` }"></div>
                  <strong>{{ m.high.toFixed(2) }}</strong>
                </div>
              </div>
            </div>
          </div>

          <p class="note">Descriptive slice analysis within the code-switched Pidgin population; not a causal estimate of code-switching effects.</p>
        </section>

        <section class="panel">
          <div class="section-head">
            <div>
              <p class="eyebrow">6 · Robustness</p>
              <h2>What about more switching points?</h2>
              <p class="section-copy">WER is shown for lower versus higher switch-point groups.</p>
            </div>
          </div>

          <div class="mini-chart">
            <div v-for="m in data.switch" :key="`switch-${m.model}`" class="mini-row">
              <div class="mini-name">{{ m.model }}</div>
              <div class="mini-bars">
                <div class="mini-track">
                  <span class="mini-caption">Low</span>
                  <div class="mini-fill" :style="{ width: `${miniWidth(m.low)}%` }"></div>
                  <strong>{{ m.low.toFixed(2) }}</strong>
                </div>
                <div class="mini-track">
                  <span class="mini-caption">High</span>
                  <div class="mini-fill high" :style="{ width: `${miniWidth(m.high)}%` }"></div>
                  <strong>{{ m.high.toFixed(2) }}</strong>
                </div>
              </div>
            </div>
          </div>

          <p class="note">These are descriptive WER slices, not a causal estimate of switching complexity.</p>
        </section>
      </section>

      <!-- Dataset composition -->
      <section class="panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">7 · Know the data</p>
            <h2>The Pidgin test split is overwhelmingly code-switched</h2>
            <p class="section-copy">This matters when interpreting the benchmark.</p>
          </div>
        </div>

        <div class="dataset-visual">
          <div class="dataset-total">
            <div class="dataset-number">1,801</div>
            <div class="text-sm text-ink-soft">Pidgin test utterances</div>
          </div>
          <div class="composition">
            <div class="composition-track">
              <div class="composition-main" :style="{ width: `${codeSwitchShare}%` }"></div>
              <div class="composition-control" :style="{ width: `${nonCodeSwitchShare}%` }"></div>
            </div>
            <div class="composition-legend">
              <div><span class="legend-dot main"></span><strong>1,799</strong> code-switched (99.89%)</div>
              <div><span class="legend-dot control"></span><strong>2</strong> non-code-switched (0.11%)</div>
            </div>
          </div>
        </div>

        <div class="method-grid">
          <div>
            <div class="method-number">100</div>
            <div class="method-label">utterances evaluated</div>
          </div>
          <div>
            <div class="method-number">4</div>
            <div class="method-label">ASR systems compared</div>
          </div>
          <div>
            <div class="method-number">1</div>
            <div class="method-label">fixed evaluation subset</div>
          </div>
        </div>
      </section>

      <!-- Why no CS penalty -->
      <section class="boundary">
        <div class="boundary-icon">!</div>
        <div>
          <p class="eyebrow">Methodological boundary</p>
          <h2 class="mt-1">Why we do not report a conventional code-switch penalty</h2>
          <p class="mt-3 text-ink-soft leading-relaxed">
            The full Pidgin split contains only <strong>2 non-code-switched</strong> utterances. That is not enough
            for a defensible balanced control comparison. We therefore do not manufacture a control group or turn
            two observations into a causal claim. Instead, we examine performance across CMI, switch-point count and duration.
          </p>
        </div>
      </section>

      <!-- Product connection -->
      <section class="product-panel">
        <div>
          <p class="eyebrow">Why this matters for NEUROMOYO</p>
          <h2 class="mt-1">Transcription is the first step, not the final product.</h2>
          <p class="mt-3 text-ink-soft leading-relaxed max-w-3xl">
            In the live Voice Intelligence workflow, Sahara provides the ASR layer. NEUROMOYO then extracts
            structured clinical information with evidence and combines it with the existing acoustic neurological
            screening pipeline to support clinician review.
          </p>
        </div>
        <div class="flow">
          <span>Patient speech</span><i>→</i><span>Sahara ASR</span><i>→</i><span>Clinical information</span><i>→</i><span>Clinician decision support</span>
        </div>
      </section>

      <!-- Reproducibility / limitations -->
      <section class="grid lg:grid-cols-2 gap-6">
        <section class="panel">
          <p class="eyebrow">Reproducibility</p>
          <h2 class="mt-1">How we evaluated</h2>
          <ul class="clean-list">
            <li>Fixed 100-utterance Pidgin evaluation subset.</li>
            <li>Same references and utterances for all four systems.</li>
            <li>Metrics: WER, CER, latency and real-time factor.</li>
            <li>Paired bootstrap uncertainty for Sahara comparisons.</li>
            <li>Additional CMI, switch-point and duration slice analysis.</li>
            <li>Notebook, manifests and aggregate results are available in the evidence package.</li>
          </ul>
        </section>

        <section class="panel">
          <p class="eyebrow">Read this correctly</p>
          <h2 class="mt-1">What the benchmark does — and does not — prove</h2>
          <ul class="clean-list">
            <li><strong>It does:</strong> compare ASR behaviour on this Pidgin benchmark subset.</li>
            <li><strong>It does:</strong> provide evidence for the Sahara choice in NEUROMOYO.</li>
            <li><strong>It does not:</strong> validate a clinical diagnostic model.</li>
            <li><strong>It does not:</strong> represent all African languages or accents.</li>
            <li><strong>It does not:</strong> establish a causal code-switch penalty.</li>
            <li><strong>It does not:</strong> validate the proposed Clinical Information Preservation metric.</li>
          </ul>
        </section>
      </section>

      <footer class="text-sm text-ink-soft pb-10 border-t border-mist pt-6">
        Dataset: Intron Health AfriSwitch · Pidgin · test split. Evaluation seed: 20260909.
        Results are frozen from the NEUROMOYO benchmark notebook. No raw health-related audio is published on this page.
      </footer>
    </section>
  </main>
</template>

<script setup lang="ts">
type Model = {
  model: string
  n: number
  mean_WER: number
  median_WER?: number
  mean_CER: number
  mean_latency_s: number
  mean_RTF: number
}

type Paired = {
  comparison: string
  difference: number
  low: number
  high: number
}

type Slice = {
  model: string
  low: number
  high: number
}

type BenchmarkData = {
  models: Model[]
  paired: Paired[]
  cmi: Slice[]
  switch: Slice[]
  dataset?: Record<string, unknown>
}

const fallback: BenchmarkData = {
  models: [
    { model: 'Sahara', n: 100, mean_WER: 0.52622, median_WER: 0.5, mean_CER: 0.337606, mean_latency_s: 2.48823, mean_RTF: 0.349679 },
    { model: 'MMS-1B', n: 100, mean_WER: 0.655644, median_WER: 0.617647, mean_CER: 0.365325, mean_latency_s: 0.407694, mean_RTF: 0.0470506 },
    { model: 'Whisper Tiny', n: 100, mean_WER: 2.43599, median_WER: 0.870192, mean_CER: 2.08329, mean_latency_s: 1.26068, mean_RTF: 0.16135 },
    { model: 'Whisper Base', n: 100, mean_WER: 2.84114, median_WER: 0.809091, mean_CER: 1.92592, mean_latency_s: 1.73561, mean_RTF: 0.183715 }
  ],
  paired: [
    { comparison: 'Sahara − Whisper Tiny', difference: -1.90977, low: -2.84251, high: -1.11459 },
    { comparison: 'Sahara − Whisper Base', difference: -2.31492, low: -3.28402, high: -1.48954 },
    { comparison: 'Sahara − MMS-1B', difference: -0.129424, low: -0.169516, high: -0.0905367 }
  ],
  cmi: [
    { model: 'Sahara', low: 0.520404, high: 0.532036 },
    { model: 'MMS-1B', low: 0.623452, high: 0.687836 },
    { model: 'Whisper Tiny', low: 3.10772, high: 1.76425 },
    { model: 'Whisper Base', low: 2.33611, high: 3.34617 }
  ],
  switch: [
    { model: 'Sahara', low: 0.499245, high: 0.554296 },
    { model: 'MMS-1B', low: 0.666923, high: 0.643904 },
    { model: 'Whisper Tiny', low: 2.11772, high: 2.76724 },
    { model: 'Whisper Base', low: 2.88119, high: 2.79945 }
  ]
}

const { data: loaded } = await useFetch<BenchmarkData>('/benchmark.json')
const data = computed(() => loaded.value?.models?.length ? loaded.value : fallback)

const best = computed(() => data.value.models.find(m => m.model === 'Sahara'))
const bestSpeed = computed(() => [...data.value.models].sort((a, b) => a.mean_RTF - b.mean_RTF)[0])
const maxWER = computed(() => Math.max(...data.value.models.map(m => m.mean_WER), 1))
const maxRTF = computed(() => Math.max(...data.value.models.map(m => m.mean_RTF), 0.1))
const improvementVsMMS = computed(() => {
  const sahara = best.value?.mean_WER
  const mms = data.value.models.find(m => m.model === 'MMS-1B')?.mean_WER
  return sahara != null && mms ? (((mms - sahara) / mms) * 100).toFixed(1) : '—'
})

const codeSwitchShare = 1799 / 1801 * 100
const nonCodeSwitchShare = 2 / 1801 * 100

function pct(v?: number) {
  return v == null ? '—' : `${(v * 100).toFixed(1)}%`
}

function barWidth(value: number, max: number) {
  return Math.max(2, (value / max) * 100)
}

function miniWidth(value: number) {
  const max = Math.max(...data.value.models.map(m => Math.max(m.mean_WER, 0.1)))
  return Math.max(4, (value / max) * 100)
}

function medianWER(m: Model) {
  return m.median_WER == null ? '—' : m.median_WER.toFixed(3)
}

function shortComparison(value: string) {
  return value.replace('Sahara − ', 'vs ')
}

function signed(value: number) {
  return `${value >= 0 ? '+' : ''}${value.toFixed(3)}`
}

// Fixed visual range for the paired WER differences shown in the benchmark.
function intervalPosition(value: number) {
  const min = -3.5
  const max = 0
  return Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100))
}
</script>

<style scoped>
.card,.panel{background:white;border:1px solid #e4ebe8;border-radius:1.15rem;padding:1.25rem}
.card{min-height:132px}.card.accent{background:linear-gradient(145deg,#f0f8f4,#fff);border-color:#cfe3da}
.label,.eyebrow{font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;font-weight:750;color:#5f706a}
.metric{font-size:2rem;font-weight:750;margin-top:.35rem;letter-spacing:-.03em}.hero-stat{min-width:220px;border:1px solid #d8e5e0;background:#f7fbf9;border-radius:1.25rem;padding:1.25rem}.hero-number{font-size:3.3rem;font-weight:800;letter-spacing:-.05em;line-height:1;margin:.35rem 0}
.sub,.note{font-size:.78rem;color:#6d7b77;margin-top:.3rem}.section-head{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:1.4rem}.section-head h2{font-size:1.5rem;font-weight:650;margin-top:.25rem;letter-spacing:-.02em}.section-copy{font-size:.88rem;color:#6d7b77;line-height:1.6;margin-top:.35rem;max-width:760px}
.pill,.badge{font-size:.72rem;border:1px solid #dce6e2;border-radius:999px;padding:.45rem .7rem;color:#5f706a;background:#fbfdfc}.badge{white-space:nowrap}
.takeaway{display:grid;grid-template-columns:auto 1fr;gap:1rem;align-items:start;border:1px solid #d9e8e1;background:#f5faf7;border-radius:1.15rem;padding:1.3rem}.takeaway-icon{width:42px;height:42px;border-radius:.8rem;display:grid;place-items:center;background:#dceee6;color:#236f58;font-size:.7rem;font-weight:800}.takeaway h2{font-size:1.25rem;font-weight:650;letter-spacing:-.015em}
.chart-wrap{display:grid;gap:1.05rem}.bar-row{display:grid;grid-template-columns:150px 1fr;gap:1rem;align-items:center}.bar-label{display:flex;justify-content:space-between;gap:.7rem;font-size:.86rem}.bar-value{font-variant-numeric:tabular-nums;color:#53645e;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem}.bar-track{height:15px;border-radius:999px;background:#edf2f0;overflow:hidden}.bar-fill{height:100%;border-radius:999px;background:#90aaa0;transition:width .3s ease}.bar-fill.best{background:#277c62}.bar-fill.speed{background:#a4b5ae}.bar-fill.speed.best{background:#5c746b}
.callout{display:flex;gap:.65rem;align-items:center;margin-top:1.4rem;border:1px solid #d8e9e1;background:#f6fbf8;border-radius:.8rem;padding:.8rem 1rem;font-size:.82rem;color:#52635d}.callout.neutral{background:#fafcfc;border-color:#e1e9e6}.dot{width:8px;height:8px;border-radius:50%;background:#277c62;flex:none}
table{width:100%;border-collapse:collapse;font-size:.86rem}th,td{text-align:left;padding:.9rem;border-bottom:1px solid #e7eeeb;white-space:nowrap}th{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6d7b77}.numeric{font-variant-numeric:tabular-nums;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.winner{background:#f3faf6}.winner-mark{font-size:.62rem;text-transform:uppercase;letter-spacing:.06em;background:#dceee6;color:#236f58;border-radius:999px;padding:.3rem .45rem;font-weight:800}.legend-row{display:flex;flex-wrap:wrap;gap:1.2rem;margin-top:1rem;font-size:.74rem;color:#6d7b77}
.interval-chart{position:relative;padding:1rem 0 0}.interval-row{display:grid;grid-template-columns:150px 1fr 65px;gap:1rem;align-items:center;margin:.9rem 0}.interval-label{font-size:.82rem;font-weight:600}.interval-track{position:relative;height:20px;background:#f0f4f2;border-radius:999px}.zero-line{position:absolute;top:0;bottom:30px;width:1px;background:#80918b;z-index:2}.interval{position:absolute;top:7px;height:6px;border-radius:999px;background:#6d9185}.interval-point{position:absolute;top:4px;width:12px;height:12px;border-radius:50%;background:#236f58;transform:translateX(-50%);z-index:3}.interval-value{text-align:right;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.76rem;color:#52635d}.interval-axis{display:flex;justify-content:space-between;margin-left:166px;margin-right:65px;color:#82908b;font-size:.68rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.mini-chart{display:grid;gap:.8rem}.mini-row{display:grid;grid-template-columns:90px 1fr;gap:.8rem;align-items:center}.mini-name{font-size:.78rem;font-weight:650}.mini-bars{display:grid;gap:.45rem}.mini-track{display:grid;grid-template-columns:32px 1fr 42px;gap:.45rem;align-items:center}.mini-caption{font-size:.62rem;color:#82908b;text-transform:uppercase;letter-spacing:.06em}.mini-track>strong{font-size:.7rem;text-align:right;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:600;color:#60716b}.mini-fill{height:8px;border-radius:999px;background:#9eb4ac}.mini-fill.high{background:#c2cfca}
.dataset-visual{display:grid;grid-template-columns:180px 1fr;gap:2rem;align-items:center}.dataset-number{font-size:2.8rem;font-weight:800;letter-spacing:-.04em}.composition-track{height:28px;border-radius:999px;overflow:hidden;background:#e9efec;display:flex}.composition-main{background:#277c62}.composition-control{background:#c4cfcb;min-width:2px}.composition-legend{display:flex;flex-wrap:wrap;gap:1.2rem;margin-top:.75rem;font-size:.75rem;color:#64746e}.legend-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:.35rem}.legend-dot.main{background:#277c62}.legend-dot.control{background:#c4cfcb}.method-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.4rem;padding-top:1.2rem;border-top:1px solid #e7eeeb}.method-number{font-size:1.5rem;font-weight:750}.method-label{font-size:.72rem;color:#6d7b77;margin-top:.15rem}
.boundary{display:grid;grid-template-columns:auto 1fr;gap:1rem;align-items:start;border:1px solid #e3e8e6;background:#fbfcfc;border-radius:1.15rem;padding:1.3rem}.boundary-icon{width:38px;height:38px;border-radius:.7rem;display:grid;place-items:center;background:#edf1ef;color:#5c6d67;font-weight:800}
.product-panel{border:1px solid #cfe2da;background:linear-gradient(145deg,#f4faf7,#fff);border-radius:1.15rem;padding:1.35rem}.product-panel h2{font-size:1.35rem;font-weight:650}.flow{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-top:1.1rem}.flow span{border:1px solid #d4e3dd;background:#fff;border-radius:999px;padding:.55rem .75rem;font-size:.73rem;font-weight:650}.flow i{font-style:normal;color:#7b8b85}
.clean-list{margin-top:1rem;display:grid;gap:.7rem;padding-left:1.1rem;color:#63736d;font-size:.83rem;line-height:1.55}.clean-list li::marker{color:#6e9185}

@media (max-width: 640px){
  .bar-row{grid-template-columns:105px 1fr}.interval-row{grid-template-columns:105px 1fr 52px}.interval-axis{margin-left:120px;margin-right:52px}.dataset-visual{grid-template-columns:1fr;gap:1rem}.method-grid{grid-template-columns:1fr 1fr}.mini-row{grid-template-columns:75px 1fr}
}
</style>