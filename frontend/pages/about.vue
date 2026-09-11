<template>
  <main class="about-page">
    <!-- HERO -->
    <section class="hero-shell section-card">
      <div class="hero-copy">
        <div class="eyebrow"><span class="eyebrow-dot"></span> NEUROMOYO · SCIENCE &amp; SYSTEM</div>
        <h1>Voice can become a measurable window into neurological function.</h1>
        <p class="hero-lede">
          Neuromoyo is a clinician-oriented voice intelligence platform for neurological screening.
          It combines controlled speech tasks, acoustic analysis, machine learning and—when enabled—
          African-focused speech recognition to turn a short recording into evidence a clinician can inspect.
        </p>
        <div class="hero-actions">
          <NuxtLink to="/welcome" class="primary-link">Explore the product <span>→</span></NuxtLink>
          <NuxtLink to="/benchmark" class="secondary-link">See benchmark evidence</NuxtLink>
        </div>
        <div class="hero-trust-row">
          <div><strong>Screening</strong><span>not autonomous diagnosis</span></div>
          <div><strong>Explainable</strong><span>feature-level evidence</span></div>
          <div><strong>Privacy-aware</strong><span>temporary audio processing</span></div>
        </div>
      </div>

      <div class="hero-visual" aria-label="Neuromoyo scientific signal pipeline">
        <div class="orbital orbital-a"></div>
        <div class="orbital orbital-b"></div>
        <div class="signal-center">
          <span class="signal-kicker">PATIENT VOICE</span>
          <div class="waveform" aria-hidden="true">
            <i v-for="n in 19" :key="n" :style="{ height: `${18 + ((n * 17) % 42)}px` }"></i>
          </div>
          <strong>Speech → signal → evidence</strong>
        </div>
        <div class="floating-node node-one"><span>01</span><strong>Audio</strong><small>capture</small></div>
        <div class="floating-node node-two"><span>02</span><strong>Acoustics</strong><small>biomarkers</small></div>
        <div class="floating-node node-three"><span>03</span><strong>Model</strong><small>risk signal</small></div>
        <div class="floating-node node-four"><span>04</span><strong>Review</strong><small>clinician</small></div>
      </div>
    </section>

    <!-- SCIENTIFIC THESIS -->
    <section class="section-card science-thesis">
      <div class="section-heading">
        <div>
          <p class="eyebrow">01 · Scientific rationale</p>
          <h2>Why study speech in Parkinsonian motor dysfunction?</h2>
        </div>
        <p class="section-intro">
          Parkinsonian speech is not one single acoustic phenomenon. It can involve interacting changes in
          phonation, articulation, prosody, timing and respiratory support. That makes speech attractive for
          quantitative measurement—but also makes single-feature claims scientifically weak.
        </p>
      </div>

      <div class="mechanism-diagram" role="img" aria-label="Scientific pathway from motor control changes to measurable speech signals">
        <div class="mechanism-column">
          <div class="diagram-label">BIOLOGICAL SYSTEM</div>
          <div class="mechanism-box biological">
            <span class="box-icon">01</span>
            <strong>Motor control networks</strong>
            <p>Neurological motor impairment can affect the control of respiration, phonation and articulation.</p>
          </div>
          <div class="connector-v"><span>influences</span></div>
          <div class="mechanism-box biological-soft">
            <span class="box-icon">02</span>
            <strong>Laryngeal + articulatory control</strong>
            <p>Fine control of vocal intensity, pitch, timing and speech movements can become less precise.</p>
          </div>
        </div>

        <div class="mechanism-middle">
          <div class="connector-h left"><span>motor expression</span></div>
          <div class="brain-ring">
            <div class="brain-core">VOICE<br /><small>as a digital signal</small></div>
          </div>
          <div class="connector-h right"><span>observable output</span></div>
        </div>

        <div class="mechanism-column">
          <div class="diagram-label">MEASURABLE SIGNAL</div>
          <div class="feature-stack">
            <div class="feature-pill"><b>Phonation</b><span>F0 · jitter · shimmer · HNR</span></div>
            <div class="feature-pill"><b>Prosody</b><span>pitch range · intensity · pauses</span></div>
            <div class="feature-pill"><b>Articulation</b><span>DDK rate · timing · spectral cues</span></div>
            <div class="feature-pill"><b>Speech output</b><span>rate · fluency · linguistic evidence</span></div>
          </div>
        </div>
      </div>

      <div class="evidence-callout">
        <div class="evidence-mark">i</div>
        <div>
          <strong>What the literature supports</strong>
          <p>
            Reviews report measurable differences in multiple voice and speech dimensions in Parkinson's disease,
            including pitch/intensity variation, articulation rate, pause behaviour, jitter and shimmer. The same
            literature also emphasises heterogeneity and the need for better longitudinal, external and clinically
            validated studies. Neuromoyo therefore treats speech as a <em>screening signal</em>, not a disease label.
          </p>
        </div>
      </div>
    </section>

    <!-- TASKS -->
    <section class="section-card">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">02 · Measurement design</p>
          <h2>Three tasks, three complementary views of speech motor function.</h2>
        </div>
        <p class="section-intro">The workflow deliberately avoids reducing a neurological voice screen to one acoustic measurement.</p>
      </div>

      <div class="task-grid">
        <article class="task-card">
          <div class="task-number">A</div>
          <div class="task-visual reading-visual"><span>READ</span><i></i><i></i><i></i><i></i><i></i></div>
          <h3>Connected speech</h3>
          <p>Reading provides a structured sample from which voice quality, timing and speech-level patterns can be measured.</p>
          <ul><li>prosodic variation</li><li>speech timing</li><li>acoustic feature vector</li></ul>
        </article>

        <article class="task-card featured">
          <div class="task-number">B</div>
          <div class="task-visual vowel-visual"><span>AAAA</span><div class="vowel-wave"></div></div>
          <h3>Sustained vowel</h3>
          <p>A sustained phonation task isolates voice production so periodicity and stability-related measures can be examined.</p>
          <ul><li>F0-related measures</li><li>jitter / shimmer</li><li>harmonic-noise characteristics</li></ul>
        </article>

        <article class="task-card">
          <div class="task-number">C</div>
          <div class="task-visual ddk-visual"><b>PA</b><b>TA</b><b>KA</b><b>PA</b><b>TA</b></div>
          <h3>Rapid syllable repetition</h3>
          <p>Diadochokinetic speech stresses rapid, alternating articulatory movements and their temporal regularity.</p>
          <ul><li>repetition rate</li><li>timing regularity</li><li>motor speech signal</li></ul>
        </article>
      </div>
    </section>

    <!-- FEATURE FAMILIES -->
    <section class="section-card feature-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">03 · From waveform to features</p>
          <h2>What the model actually sees</h2>
        </div>
        <p class="section-intro">
          The deployed acoustic pipeline uses eGeMAPS-style voice descriptors and a Logistic Regression classifier.
          SHAP is then used to expose feature-level contributions rather than presenting an unexplained score.
        </p>
      </div>

      <div class="feature-pipeline">
        <div class="pipeline-stage input-stage">
          <div class="stage-index">01</div>
          <strong>Audio waveform</strong>
          <div class="mini-wave"><i v-for="n in 26" :key="n" :style="{ height: `${10 + ((n * 13) % 30)}px` }"></i></div>
          <small>normalised recording</small>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-stage">
          <div class="stage-index">02</div>
          <strong>Acoustic descriptors</strong>
          <div class="descriptor-grid">
            <span>F0</span><span>jitter</span><span>shimmer</span><span>HNR</span><span>loudness</span><span>spectral</span>
          </div>
          <small>voice quality + prosody</small>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-stage model-stage">
          <div class="stage-index">03</div>
          <strong>ML classifier</strong>
          <div class="model-box"><b>Logistic</b><span>Regression</span></div>
          <small>probabilistic screening signal</small>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-stage explain-stage">
          <div class="stage-index">04</div>
          <strong>SHAP explanation</strong>
          <div class="shap-bars"><i style="width:84%"></i><i style="width:61%"></i><i style="width:43%"></i><i style="width:27%"></i></div>
          <small>feature contribution</small>
        </div>
      </div>

      <div class="feature-family-grid">
        <article><span class="family-icon">F₀</span><div><h3>Pitch &amp; prosody</h3><p>Fundamental-frequency level and variation help characterise pitch control and prosodic range.</p></div></article>
        <article><span class="family-icon">J</span><div><h3>Periodicity</h3><p>Jitter captures cycle-to-cycle frequency perturbation; shimmer captures amplitude perturbation.</p></div></article>
        <article><span class="family-icon">H/N</span><div><h3>Harmonic structure</h3><p>Harmonic-to-noise measures provide information about periodic versus noisy components of phonation.</p></div></article>
        <article><span class="family-icon">L</span><div><h3>Loudness &amp; energy</h3><p>Intensity-related measures can reflect the reduced loudness and restricted vocal dynamics reported in Parkinsonian speech.</p></div></article>
      </div>
    </section>

    <!-- ML + EXPLAINABILITY -->
    <section class="section-card model-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">04 · Statistical learning</p>
          <h2>A model is useful only when its output can be interrogated.</h2>
        </div>
        <p class="section-intro">Neuromoyo separates prediction from interpretation: the classifier estimates a screening signal; SHAP helps show which input features pushed the estimate.</p>
      </div>

      <div class="model-diagram">
        <div class="model-inputs">
          <div class="input-chip"><b>x₁</b> pitch</div>
          <div class="input-chip"><b>x₂</b> jitter</div>
          <div class="input-chip"><b>x₃</b> shimmer</div>
          <div class="input-chip"><b>x₄</b> loudness</div>
          <div class="input-chip"><b>x₅</b> spectral</div>
          <div class="input-chip"><b>…</b> other descriptors</div>
        </div>
        <div class="model-equation">
          <span>feature vector</span>
          <strong>f(x) = σ(w·x + b)</strong>
          <small>Logistic Regression</small>
        </div>
        <div class="model-output">
          <div class="risk-ring"><span>risk<br /><b>signal</b></span></div>
          <div><strong>Clinician-facing result</strong><p>Not a diagnosis. A prompt for closer review within the clinical pathway.</p></div>
        </div>
      </div>

      <div class="explain-grid">
        <div class="explain-graphic">
          <div class="zero-line"></div>
          <div class="explain-row"><span>feature A</span><i class="positive" style="width:74%"></i><b>+</b></div>
          <div class="explain-row"><span>feature B</span><i class="negative" style="width:53%"></i><b>−</b></div>
          <div class="explain-row"><span>feature C</span><i class="positive" style="width:39%"></i><b>+</b></div>
          <div class="explain-row"><span>feature D</span><i class="negative" style="width:24%"></i><b>−</b></div>
          <div class="explain-axis"><span>lower contribution</span><span>higher contribution</span></div>
        </div>
        <div class="explain-copy">
          <p class="eyebrow">Interpretability layer</p>
          <h3>SHAP answers a different question from the classifier.</h3>
          <p>
            A screening model can output a probability-like score without explaining itself. SHAP values provide a
            consistent way to attribute an individual prediction to model features. In Neuromoyo, this is presented as
            supporting evidence for clinician review—not as proof that a particular feature is caused by Parkinson's disease.
          </p>
          <div class="boundary-note"><b>Interpretation boundary:</b> feature contribution ≠ biological causation ≠ clinical diagnosis.</div>
        </div>
      </div>
    </section>

    <!-- VOICE INTELLIGENCE -->
    <section class="section-card intelligence-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">05 · African voice intelligence</p>
          <h2>Speech recognition is a layer—not the clinical endpoint.</h2>
        </div>
        <p class="section-intro">
          Neuromoyo's competition-facing Voice Intelligence workflow adds African-focused ASR to the clinical pipeline.
          Sahara is evaluated as an information-preserving speech interface: transcription feeds downstream clinical information extraction rather than ending the workflow.
        </p>
      </div>

      <div class="intelligence-diagram">
        <div class="int-node speech-node"><span>01</span><strong>Natural speech</strong><small>patient voice</small></div>
        <div class="int-arrow">→</div>
        <div class="int-node"><span>02</span><strong>Audio QC</strong><small>quality + consent</small></div>
        <div class="int-arrow">→</div>
        <div class="int-node sahara-node"><span>03</span><strong>Sahara ASR</strong><small>African speech recognition</small></div>
        <div class="int-arrow">→</div>
        <div class="int-node"><span>04</span><strong>Clinical information</strong><small>findings + evidence</small></div>
        <div class="int-arrow">→</div>
        <div class="int-node output-node"><span>05</span><strong>Clinician review</strong><small>decision support</small></div>
      </div>

      <div class="intelligence-principles">
        <article><b>Transcription is not diagnosis</b><p>Lower ASR error does not automatically mean better clinical utility. The downstream information task matters.</p></article>
        <article><b>Evidence stays attached</b><p>Clinical findings can retain transcript evidence so a reviewer can inspect where an extracted finding came from.</p></article>
        <article><b>Acoustic and linguistic signals are complementary</b><p>The acoustic screening pathway and ASR pathway answer different questions and should not be conflated.</p></article>
      </div>
    </section>

    <!-- BENCHMARK SCIENCE -->
    <section class="section-card benchmark-science">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">06 · Research evidence</p>
          <h2>Benchmarking the speech layer under African code-switching.</h2>
        </div>
        <NuxtLink to="/benchmark" class="inline-link">Open the full benchmark →</NuxtLink>
      </div>

      <div class="benchmark-layout">
        <div class="benchmark-bars">
          <div class="chart-title"><strong>Mean WER</strong><span>lower is better</span></div>
          <div v-for="item in benchmarkModels" :key="item.name" class="bar-row">
            <span>{{ item.name }}</span>
            <div class="bar-track"><i :style="{ width: `${Math.min(100, (item.wer / 3) * 100)}%` }"></i></div>
            <b>{{ item.wer.toFixed(2) }}</b>
          </div>
          <div class="chart-foot">100 Pidgin utterances · same evaluation subset · WER is not a clinical validity measure.</div>
        </div>

        <div class="benchmark-stat-card">
          <span class="stat-label">Sahara mean WER</span>
          <strong>0.526</strong>
          <p>Lowest mean WER among the four evaluated systems in the current benchmark.</p>
          <div class="stat-divider"></div>
          <span class="stat-label">MMS-1B mean RTF</span>
          <strong>0.047</strong>
          <p>Fastest real-time factor in the same benchmark—showing that accuracy and speed are separate engineering dimensions.</p>
        </div>
      </div>

      <div class="research-boundary">
        <div class="boundary-icon">!</div>
        <div><strong>What this benchmark can—and cannot—claim</strong><p>The evaluation compares ASR behaviour on a defined Pidgin subset. It does not establish clinical accuracy, population representativeness, or superiority across African languages. The available Pidgin test split is overwhelmingly code-switched, so Neuromoyo does not invent a conventional code-switching penalty from an artificial control group.</p></div>
      </div>
    </section>

    <!-- CLINICAL PIPELINE -->
    <section class="section-card clinical-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">07 · Clinical workflow</p>
          <h2>Designed to support a human decision, not replace one.</h2>
        </div>
        <p class="section-intro">The product boundary is deliberate: the model produces evidence; the clinician owns the clinical interpretation.</p>
      </div>

      <div class="clinical-flow">
        <div class="clinical-step"><span>01</span><b>Consent</b><p>Patient agrees to voice capture and analysis.</p></div>
        <div class="flow-arrow">↓</div>
        <div class="clinical-step"><span>02</span><b>Capture</b><p>Short structured speech tasks are recorded.</p></div>
        <div class="flow-arrow">↓</div>
        <div class="clinical-step"><span>03</span><b>Analyse</b><p>Audio is quality-checked and transformed into measurable signals.</p></div>
        <div class="flow-arrow">↓</div>
        <div class="clinical-step"><span>04</span><b>Review</b><p>Risk signal, findings, provenance and explanations are presented.</p></div>
        <div class="flow-arrow">↓</div>
        <div class="clinical-step final-step"><span>05</span><b>Clinical action</b><p>Referral, follow-up or further assessment remains a human decision.</p></div>
      </div>
    </section>

    <!-- LIMITATIONS -->
    <section class="section-card limitations-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">08 · Scientific boundaries</p>
          <h2>What we deliberately do not claim.</h2>
        </div>
      </div>
      <div class="limits-grid">
        <article><span>01</span><h3>Not a diagnostic device</h3><p>The current system is a screening and decision-support workflow. A model score does not establish Parkinson's disease.</p></article>
        <article><span>02</span><h3>Not language-neutral by default</h3><p>Voice biomarkers can be affected by language, accent, recording conditions, age, sex, medication state and other confounders. Broader validation is required.</p></article>
        <article><span>03</span><h3>Not validated by ASR WER</h3><p>Speech recognition performance and clinical validity are different questions. Benchmark WER/CER is evidence about the ASR layer only.</p></article>
        <article><span>04</span><h3>Not a replacement for longitudinal evidence</h3><p>Longitudinal monitoring is promising, but robust clinical use requires prospective validation, calibration and external evaluation.</p></article>
      </div>
    </section>

    <!-- RESPONSIBLE AI -->
    <section class="section-card safety-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">09 · Responsible AI</p>
          <h2>Safety is part of the architecture.</h2>
        </div>
      </div>
      <div class="safety-grid">
        <article><div class="safety-icon">C</div><h3>Consent</h3><p>Voice analysis is gated by explicit consent in the Voice Intelligence workflow.</p></article>
        <article><div class="safety-icon">P</div><h3>Privacy</h3><p>Raw audio is processed temporarily and is not intended to become a permanent patient-media archive.</p></article>
        <article><div class="safety-icon">E</div><h3>Evidence</h3><p>Findings retain provenance and supporting transcript evidence where the linguistic pathway is used.</p></article>
        <article><div class="safety-icon">H</div><h3>Human oversight</h3><p>The output is framed as decision support for trained healthcare personnel.</p></article>
      </div>
    </section>

    <!-- REFERENCES -->
    <section class="section-card references-section">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">10 · Scientific references</p>
          <h2>Evidence behind the design.</h2>
        </div>
        <p class="section-intro">The references below support the scientific rationale; they do not constitute validation of the Neuromoyo system itself.</p>
      </div>
      <ol class="references">
        <li><span>[1]</span><div><strong>Speech and language biomarkers for Parkinson's disease prediction, early diagnosis and progression.</strong><small>Renteria et al., 2025 · Review of speech/language features and their potential across the PD continuum.</small><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11933288/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
        <li><span>[2]</span><div><strong>From prodromal stages to clinical trials: The promise of digital speech biomarkers in Parkinson's disease.</strong><small>2024 review · discusses voice quality, pitch, loudness and articulation as digital speech biomarkers.</small><a href="https://pubmed.ncbi.nlm.nih.gov/39424108/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
        <li><span>[3]</span><div><strong>Acoustic analysis of voice in Parkinson's disease: systematic review and meta-analysis.</strong><small>Chiaramonte &amp; Bonfiglio, 2020 · reports evidence around jitter, shimmer, F0 variation and other acoustic measures, with heterogeneity across studies.</small><a href="https://pubmed.ncbi.nlm.nih.gov/32436206/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
        <li><span>[4]</span><div><strong>Guidelines for Speech Recording and Acoustic Analyses in Dysarthrias of Movement Disorders.</strong><small>2020 · provides recommendations around recording conditions, vocal tasks and acoustic outcomes.</small><a href="https://pubmed.ncbi.nlm.nih.gov/33373483/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
        <li><span>[5]</span><div><strong>A Systematic Review and Bayesian Meta-Analysis of Acoustic Measures of Prosody in Parkinson's Disease.</strong><small>2024 · synthesises evidence for F0, intensity, articulation rate and pause-related measures.</small><a href="https://pubmed.ncbi.nlm.nih.gov/39018262/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
        <li><span>[6]</span><div><strong>Voice-Based Detection of Parkinson’s Disease Using Machine and Deep Learning Approaches: A Systematic Review.</strong><small>Recent systematic review · highlights the breadth of ML approaches while reinforcing the need for careful clinical translation.</small><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC12649940/" target="_blank" rel="noopener noreferrer">Read source →</a></div></li>
      </ol>
    </section>

    <footer class="about-footer">
      <div><span class="footer-mark">N</span><strong>NEUROMOYO</strong></div>
      <p>Voice intelligence for African neurological care · Screening support, not autonomous diagnosis.</p>
      <NuxtLink to="/benchmark">Inspect the evidence →</NuxtLink>
    </footer>
  </main>
</template>

<script setup lang="ts">
const benchmarkModels = [
  { name: 'Sahara', wer: 0.52622 },
  { name: 'MMS-1B', wer: 0.655644 },
  { name: 'Whisper Tiny', wer: 2.43599 },
  { name: 'Whisper Base', wer: 2.84114 },
]
</script>

<style scoped>
.about-page {
  --page-bg: #f6faf8;
  --surface: rgba(255,255,255,.88);
  --surface-strong: #fff;
  --ink: var(--color-ink, #142520);
  --muted: var(--color-ink-soft, #5c6d67);
  --mist: var(--color-mist, #dce8e3);
  --teal: var(--color-teal-600, #0e6b5c);
  --teal-dark: var(--color-teal-700, #095447);
  --teal-soft: var(--color-teal-50, #e9f7f3);
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  color: var(--ink);
  padding-bottom: 2rem;
}

.section-card {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--mist);
  border-radius: 1.55rem;
  background: var(--surface);
  box-shadow: 0 18px 55px rgba(20,37,32,.055);
  backdrop-filter: blur(12px);
}

.hero-shell {
  min-height: 600px;
  display: grid;
  grid-template-columns: minmax(0, 1.06fr) minmax(420px, .94fr);
  align-items: stretch;
  background:
    radial-gradient(circle at 85% 35%, rgba(14,107,92,.13), transparent 32%),
    linear-gradient(135deg, rgba(255,255,255,.96), rgba(233,247,243,.72));
}

.hero-copy { padding: clamp(1.5rem, 5vw, 4.2rem); display:flex; flex-direction:column; justify-content:center; }
.eyebrow { margin:0; font-size:.7rem; font-weight:800; letter-spacing:.16em; text-transform:uppercase; color:var(--teal); }
.eyebrow-dot { display:inline-block; width:.45rem; height:.45rem; margin-right:.45rem; border-radius:50%; background:var(--teal); box-shadow:0 0 0 5px rgba(14,107,92,.1); }
.hero-copy h1, .section-heading h2 { font-family:var(--font-display); letter-spacing:-.035em; }
.hero-copy h1 { max-width: 10ch; margin:.7rem 0 1.15rem; font-size:clamp(2.7rem, 5.7vw, 5.7rem); line-height:.94; }
.hero-lede { max-width:65ch; margin:0; color:var(--muted); font-size:clamp(1rem,1.5vw,1.16rem); line-height:1.75; }
.hero-actions { display:flex; flex-wrap:wrap; gap:.75rem; margin-top:1.55rem; }
.primary-link,.secondary-link,.inline-link { display:inline-flex; align-items:center; gap:.55rem; border-radius:999px; padding:.85rem 1.15rem; font-weight:750; transition:.18s ease; }
.primary-link { color:#fff; background:var(--teal); box-shadow:0 14px 32px rgba(14,107,92,.18); }
.secondary-link { color:var(--ink); background:#fff; border:1px solid var(--mist); }
.primary-link:hover,.secondary-link:hover,.inline-link:hover { transform:translateY(-2px); }
.primary-link:hover { background:var(--teal-dark); }
.hero-trust-row { display:grid; grid-template-columns:repeat(3,1fr); max-width:650px; margin-top:2.2rem; border-top:1px solid var(--mist); padding-top:1rem; gap:1rem; }
.hero-trust-row div { display:flex; flex-direction:column; gap:.22rem; }
.hero-trust-row strong { font-size:.84rem; }
.hero-trust-row span { color:var(--muted); font-size:.72rem; }

.hero-visual { position:relative; min-height:600px; display:grid; place-items:center; overflow:hidden; background:linear-gradient(160deg,rgba(9,84,71,.98),rgba(13,107,92,.94)); }
.hero-visual:before { content:""; position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 92%); }
.orbital { position:absolute; border:1px solid rgba(255,255,255,.17); border-radius:50%; transform:rotate(-16deg); }
.orbital-a { width:72%; aspect-ratio:1; }
.orbital-b { width:50%; aspect-ratio:1; transform:rotate(52deg); }
.signal-center { z-index:2; width:min(300px,55%); aspect-ratio:1; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:#fff; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.25); box-shadow:0 25px 80px rgba(0,0,0,.18),inset 0 0 60px rgba(255,255,255,.04); backdrop-filter:blur(9px); }
.signal-kicker { font-size:.62rem; letter-spacing:.18em; opacity:.7; }
.signal-center strong { font-size:.95rem; margin-top:.75rem; }
.waveform { height:52px; display:flex; align-items:center; gap:4px; margin-top:1rem; }
.waveform i,.mini-wave i { width:3px; border-radius:999px; background:#b8eee2; display:block; }
.floating-node { position:absolute; z-index:3; display:flex; flex-direction:column; min-width:100px; padding:.72rem .8rem; border:1px solid rgba(255,255,255,.18); border-radius:1rem; background:rgba(255,255,255,.09); color:#fff; backdrop-filter:blur(10px); box-shadow:0 12px 30px rgba(0,0,0,.1); }
.floating-node span { font-size:.6rem; color:#a8dfd4; letter-spacing:.12em; }
.floating-node strong { font-size:.8rem; margin-top:.2rem; }
.floating-node small { opacity:.65; margin-top:.1rem; }
.node-one { top:16%; left:12%; }.node-two { top:18%; right:10%; }.node-three { bottom:17%; left:10%; }.node-four { bottom:15%; right:11%; }

.section-heading { display:grid; grid-template-columns:minmax(0,1.1fr) minmax(280px,.9fr); gap:2rem; align-items:end; padding:2rem 2rem 1rem; }
.section-heading.compact { padding-bottom:.5rem; }
.section-heading h2 { margin:.45rem 0 0; font-size:clamp(1.85rem,3.4vw,3.1rem); line-height:1.02; max-width:18ch; }
.section-intro { margin:0; color:var(--muted); line-height:1.75; }

.science-thesis { padding-bottom:1.35rem; }
.mechanism-diagram { margin:1.2rem 2rem 1.3rem; padding:1.4rem; display:grid; grid-template-columns:1fr minmax(160px,.55fr) 1fr; gap:1rem; align-items:center; border:1px solid var(--mist); border-radius:1.2rem; background:linear-gradient(180deg,#fff,#f5faf8); }
.diagram-label { font-size:.62rem; letter-spacing:.13em; font-weight:800; color:var(--muted); margin-bottom:.55rem; }
.mechanism-box { border:1px solid var(--mist); border-radius:1rem; padding:1rem; background:#fff; box-shadow:0 8px 24px rgba(20,37,32,.04); }
.mechanism-box strong { display:block; margin:.5rem 0 .35rem; }.mechanism-box p { margin:0; color:var(--muted); font-size:.82rem; line-height:1.55; }
.box-icon,.task-number,.stage-index { display:grid; place-items:center; width:2rem; height:2rem; border-radius:.65rem; background:var(--teal-soft); color:var(--teal); font-size:.65rem; font-weight:800; }
.connector-v { height:28px; width:2px; margin:auto; background:linear-gradient(var(--mist),var(--teal)); position:relative; }.connector-v span { position:absolute; left:.7rem; top:6px; width:80px; color:var(--muted); font-size:.6rem; }
.mechanism-middle { display:flex; align-items:center; gap:.55rem; justify-content:center; }
.connector-h { height:1px; flex:1; background:var(--mist); position:relative; }.connector-h span { position:absolute; top:-1.2rem; width:100px; color:var(--muted); font-size:.56rem; text-align:center; }.connector-h.left span { right:0; }.connector-h.right span { left:0; }
.brain-ring { width:115px; aspect-ratio:1; border-radius:50%; display:grid; place-items:center; background:radial-gradient(circle,#fff 0 35%,var(--teal-soft) 36% 58%,transparent 59%),conic-gradient(from 10deg,transparent 0 12%,rgba(14,107,92,.3) 13% 16%,transparent 17% 30%,rgba(14,107,92,.3) 31% 34%,transparent 35% 100%); border:1px solid rgba(14,107,92,.2); }
.brain-core { text-align:center; font-weight:900; font-size:.85rem; line-height:1.1; }.brain-core small { color:var(--muted); font-size:.52rem; font-weight:500; }
.feature-stack { display:grid; gap:.5rem; }.feature-pill { display:flex; justify-content:space-between; align-items:center; gap:.6rem; padding:.72rem .8rem; border:1px solid var(--mist); border-radius:.8rem; background:#fff; }.feature-pill b { font-size:.76rem; }.feature-pill span { color:var(--muted); font-size:.64rem; text-align:right; }
.evidence-callout,.research-boundary { margin:0 2rem; display:flex; gap:.9rem; padding:1rem; border-radius:1rem; background:var(--teal-soft); border:1px solid rgba(14,107,92,.12); }.evidence-mark,.boundary-icon { flex:0 0 auto; width:2rem; height:2rem; display:grid; place-items:center; border-radius:50%; background:var(--teal); color:#fff; font-weight:800; }.evidence-callout strong,.research-boundary strong { display:block; margin:.1rem 0 .25rem; }.evidence-callout p,.research-boundary p { margin:0; color:var(--muted); font-size:.83rem; line-height:1.65; }

.task-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; padding:1rem 2rem 2rem; }
.task-card { position:relative; padding:1.2rem; border:1px solid var(--mist); border-radius:1.2rem; background:#fff; overflow:hidden; }.task-card.featured { background:linear-gradient(145deg,var(--teal-soft),#fff); border-color:rgba(14,107,92,.18); }.task-number { margin-bottom:1rem; }
.task-card h3 { margin:1rem 0 .4rem; font-size:1.05rem; }.task-card p { margin:0; color:var(--muted); line-height:1.6; font-size:.84rem; }.task-card ul { margin:.85rem 0 0; padding-left:1rem; color:var(--muted); font-size:.74rem; line-height:1.8; }
.task-visual { height:120px; border-radius:1rem; background:#f3f8f6; border:1px solid var(--mist); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden; }.reading-visual { gap:6px; align-items:flex-end; padding:0 1.2rem 1.8rem; }.reading-visual span { position:absolute; top:.75rem; left:.8rem; font-size:.58rem; letter-spacing:.15em; color:var(--teal); font-weight:800; }.reading-visual i { width:8px; border-radius:5px 5px 1px 1px; background:var(--teal); opacity:.8; }.reading-visual i:nth-of-type(1){height:22px}.reading-visual i:nth-of-type(2){height:39px}.reading-visual i:nth-of-type(3){height:31px}.reading-visual i:nth-of-type(4){height:53px}.reading-visual i:nth-of-type(5){height:42px}
.vowel-visual span { font-size:1.6rem; letter-spacing:.16em; font-weight:800; color:var(--teal); }.vowel-wave { position:absolute; width:80%; height:35px; bottom:12px; border-top:2px solid var(--teal); border-radius:50%; transform:skewY(-3deg); opacity:.5; }.ddk-visual { gap:.45rem; }.ddk-visual b { display:grid; place-items:center; width:42px; height:42px; border-radius:50%; color:var(--teal); background:#fff; border:1px solid rgba(14,107,92,.2); font-size:.7rem; }

.feature-section,.model-section,.intelligence-section,.benchmark-science,.clinical-section,.limitations-section,.safety-section,.references-section { padding-bottom:1.5rem; }
.feature-pipeline { display:grid; grid-template-columns:1fr auto 1.1fr auto 1fr auto 1fr; gap:.65rem; align-items:center; padding:1rem 2rem; }
.pipeline-stage { min-height:190px; padding:1rem; border:1px solid var(--mist); border-radius:1.1rem; background:#fff; }.pipeline-stage strong { display:block; margin:.65rem 0 .8rem; }.pipeline-stage small { display:block; margin-top:.75rem; color:var(--muted); font-size:.65rem; }.pipeline-arrow { color:var(--teal); font-size:1.4rem; font-weight:800; }
.mini-wave { height:48px; display:flex; align-items:center; gap:3px; }.mini-wave i { width:3px; background:var(--teal); opacity:.65; }.descriptor-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:.4rem; }.descriptor-grid span { padding:.42rem; border-radius:.5rem; background:var(--teal-soft); color:var(--teal); font-size:.62rem; text-align:center; }.model-box { display:flex; flex-direction:column; align-items:center; justify-content:center; height:80px; border-radius:.9rem; background:linear-gradient(135deg,var(--teal),#157f6e); color:#fff; }.model-box b { font-size:1.05rem; }.model-box span { font-size:.7rem; opacity:.8; }.shap-bars { display:grid; gap:.5rem; padding-top:.2rem; }.shap-bars i { height:9px; border-radius:99px; background:var(--teal); display:block; }
.feature-family-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; padding:0 2rem; }.feature-family-grid article { display:flex; gap:.75rem; padding:.9rem; border-radius:1rem; background:#f7faf9; border:1px solid var(--mist); }.family-icon { flex:0 0 auto; display:grid; place-items:center; width:2.2rem; height:2.2rem; border-radius:.7rem; background:#fff; color:var(--teal); font-size:.63rem; font-weight:900; }.feature-family-grid h3 { margin:0 0 .25rem; font-size:.8rem; }.feature-family-grid p { margin:0; color:var(--muted); font-size:.68rem; line-height:1.5; }

.model-diagram { display:grid; grid-template-columns:1fr minmax(250px,.8fr) 1fr; gap:1rem; align-items:center; margin:1rem 2rem; padding:1.2rem; border-radius:1.2rem; background:#f7faf9; border:1px solid var(--mist); }.model-inputs { display:grid; grid-template-columns:repeat(2,1fr); gap:.5rem; }.input-chip { padding:.65rem; background:#fff; border:1px solid var(--mist); border-radius:.75rem; font-size:.7rem; color:var(--muted); }.input-chip b { color:var(--teal); margin-right:.25rem; }.model-equation { text-align:center; padding:1.2rem; border-radius:1rem; background:#fff; border:1px solid var(--mist); }.model-equation span,.model-equation small { display:block; color:var(--muted); font-size:.62rem; }.model-equation strong { display:block; margin:.5rem 0; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:1.1rem; }.model-output { display:flex; gap:.75rem; align-items:center; }.risk-ring { width:90px; aspect-ratio:1; border-radius:50%; display:grid; place-items:center; flex:0 0 auto; background:conic-gradient(var(--teal) 0 68%,#dce8e3 68%); position:relative; }.risk-ring:after { content:""; position:absolute; inset:9px; border-radius:50%; background:#fff; }.risk-ring span { position:relative; z-index:1; text-align:center; font-size:.58rem; }.model-output p { margin:.25rem 0 0; color:var(--muted); font-size:.7rem; line-height:1.45; }
.explain-grid { display:grid; grid-template-columns:1.1fr .9fr; gap:1.3rem; padding:1rem 2rem 0; align-items:center; }.explain-graphic { padding:1rem; border:1px solid var(--mist); border-radius:1rem; background:#fff; }.zero-line { height:1px; background:var(--mist); margin-left:33%; }.explain-row { display:grid; grid-template-columns:30% 1fr 20px; gap:.55rem; align-items:center; margin:.7rem 0; }.explain-row span { font-size:.68rem; color:var(--muted); }.explain-row i { display:block; height:12px; border-radius:99px; }.explain-row i.positive { background:var(--teal); }.explain-row i.negative { background:#a9b8b3; margin-left:25%; }.explain-row b { font-size:.7rem; color:var(--muted); }.explain-axis { display:flex; justify-content:space-between; margin-top:.75rem; color:var(--muted); font-size:.6rem; }.explain-copy h3 { margin:.45rem 0 .6rem; font-size:1.25rem; }.explain-copy p { color:var(--muted); line-height:1.7; font-size:.86rem; }.boundary-note { padding:.8rem; border-left:3px solid var(--teal); background:var(--teal-soft); color:var(--muted); font-size:.76rem; line-height:1.55; }

.intelligence-diagram { display:grid; grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr; gap:.45rem; align-items:center; padding:1rem 2rem; }.int-node { min-height:130px; padding:.9rem; border:1px solid var(--mist); border-radius:1rem; background:#fff; display:flex; flex-direction:column; justify-content:center; }.int-node span { font-size:.6rem; color:var(--teal); font-weight:800; }.int-node strong { margin:.35rem 0; font-size:.78rem; }.int-node small { color:var(--muted); font-size:.61rem; line-height:1.4; }.sahara-node { background:var(--teal-soft); border-color:rgba(14,107,92,.2); box-shadow:0 10px 30px rgba(14,107,92,.08); }.output-node { background:#f7faf9; }.int-arrow { color:var(--teal); font-size:1.2rem; font-weight:800; }.intelligence-principles { display:grid; grid-template-columns:repeat(3,1fr); gap:.75rem; padding:0 2rem; }.intelligence-principles article { padding:.9rem; border-top:2px solid var(--teal); background:#f8fbfa; border-radius:.6rem; }.intelligence-principles b { font-size:.8rem; }.intelligence-principles p { margin:.35rem 0 0; color:var(--muted); font-size:.7rem; line-height:1.55; }

.benchmark-layout { display:grid; grid-template-columns:1.25fr .75fr; gap:1rem; padding:1rem 2rem; }.benchmark-bars,.benchmark-stat-card { border:1px solid var(--mist); border-radius:1.1rem; background:#fff; padding:1rem; }.chart-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; }.chart-title span { color:var(--muted); font-size:.65rem; }.bar-row { display:grid; grid-template-columns:90px 1fr 55px; gap:.7rem; align-items:center; margin:.8rem 0; }.bar-row > span { font-size:.68rem; font-weight:700; }.bar-track { height:14px; background:#edf3f0; border-radius:99px; overflow:hidden; }.bar-track i { display:block; height:100%; border-radius:99px; background:linear-gradient(90deg,var(--teal),#61b8a8); }.bar-row b { text-align:right; font-size:.7rem; }.chart-foot { margin-top:1rem; color:var(--muted); font-size:.62rem; line-height:1.5; }.stat-label { display:block; color:var(--teal); text-transform:uppercase; letter-spacing:.12em; font-size:.58rem; font-weight:800; }.benchmark-stat-card > strong { display:block; font-size:2.1rem; letter-spacing:-.04em; margin:.15rem 0; }.benchmark-stat-card p { margin:.25rem 0; color:var(--muted); font-size:.7rem; line-height:1.55; }.stat-divider { height:1px; background:var(--mist); margin:1rem 0; }.research-boundary { margin-top:.2rem; }
.inline-link { padding:.55rem .85rem; border:1px solid var(--mist); color:var(--teal); background:#fff; font-size:.75rem; }

.clinical-flow { display:grid; grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr; gap:.5rem; align-items:center; padding:1rem 2rem; }.clinical-step { min-height:150px; padding:1rem; border-radius:1rem; border:1px solid var(--mist); background:#fff; }.clinical-step span { display:grid; place-items:center; width:1.9rem; height:1.9rem; border-radius:50%; background:var(--teal-soft); color:var(--teal); font-size:.62rem; font-weight:800; }.clinical-step b { display:block; margin:.7rem 0 .35rem; font-size:.8rem; }.clinical-step p { margin:0; color:var(--muted); font-size:.68rem; line-height:1.55; }.final-step { background:var(--teal-soft); border-color:rgba(14,107,92,.2); }.flow-arrow { color:var(--teal); font-weight:800; }

.limits-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; padding:1rem 2rem; }.limits-grid article { padding:1rem; border:1px solid var(--mist); border-radius:1rem; background:#fff; }.limits-grid span { color:var(--teal); font-weight:900; font-size:.65rem; }.limits-grid h3 { font-size:.82rem; margin:.5rem 0 .35rem; }.limits-grid p { margin:0; color:var(--muted); font-size:.7rem; line-height:1.6; }
.safety-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.75rem; padding:1rem 2rem; }.safety-grid article { padding:1rem; border-radius:1rem; background:#f7faf9; border:1px solid var(--mist); }.safety-icon { width:2rem; height:2rem; display:grid; place-items:center; border-radius:.65rem; color:var(--teal); background:var(--teal-soft); font-weight:900; font-size:.7rem; }.safety-grid h3 { font-size:.82rem; margin:.65rem 0 .3rem; }.safety-grid p { margin:0; color:var(--muted); font-size:.7rem; line-height:1.55; }
.references { list-style:none; margin:0; padding:1rem 2rem 0; display:grid; gap:.55rem; }.references li { display:grid; grid-template-columns:36px 1fr; gap:.7rem; padding:.85rem; border-bottom:1px solid var(--mist); }.references li > span { color:var(--teal); font-weight:800; font-size:.7rem; }.references strong { display:block; font-size:.78rem; line-height:1.4; }.references small { display:block; color:var(--muted); font-size:.68rem; line-height:1.55; margin:.2rem 0; }.references a { color:var(--teal); font-size:.65rem; font-weight:750; }.about-footer { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:1rem .25rem; color:var(--muted); }.about-footer > div { display:flex; align-items:center; gap:.5rem; color:var(--ink); font-size:.78rem; }.footer-mark { display:grid; place-items:center; width:1.8rem; height:1.8rem; border-radius:.55rem; color:#fff; background:var(--teal); font-weight:900; }.about-footer p { margin:0; font-size:.7rem; text-align:center; }.about-footer > a { color:var(--teal); font-size:.7rem; font-weight:750; white-space:nowrap; }

@media (max-width: 1100px) {
  .hero-shell { grid-template-columns:1fr; }.hero-visual { min-height:480px; }.hero-copy h1 { max-width:14ch; }
  .mechanism-diagram { grid-template-columns:1fr; }.mechanism-middle { padding:.5rem 0; }.feature-family-grid,.limits-grid,.safety-grid { grid-template-columns:repeat(2,1fr); }
  .feature-pipeline { grid-template-columns:1fr 1fr; }.pipeline-arrow { display:none; }.intelligence-diagram { grid-template-columns:repeat(3,1fr); }.int-arrow { display:none; }.clinical-flow { grid-template-columns:repeat(3,1fr); }.flow-arrow { display:none; }
}

@media (max-width: 760px) {
  .section-heading { grid-template-columns:1fr; gap:.7rem; padding:1.35rem 1rem .5rem; }.section-heading h2 { max-width:none; }
  .hero-copy { padding:1.35rem; }.hero-visual { min-height:430px; }.hero-trust-row { grid-template-columns:1fr; gap:.6rem; }.hero-copy h1 { font-size:clamp(2.35rem,12vw,4rem); }.floating-node { min-width:80px; padding:.55rem; }.node-one{left:4%;top:10%}.node-two{right:4%;top:12%}.node-three{left:4%;bottom:10%}.node-four{right:4%;bottom:10%}.signal-center{width:230px}
  .mechanism-diagram,.task-grid,.feature-pipeline,.model-diagram,.explain-grid,.intelligence-diagram,.benchmark-layout,.clinical-flow,.limits-grid,.safety-grid,.feature-family-grid { margin-left:1rem; margin-right:1rem; padding-left:0; padding-right:0; }.mechanism-diagram { padding:1rem; }.mechanism-middle { flex-wrap:wrap; }.connector-h { min-width:30px; }.connector-h span { display:none; }
  .task-grid,.feature-family-grid,.limits-grid,.safety-grid,.intelligence-principles { grid-template-columns:1fr; padding-left:1rem; padding-right:1rem; }.feature-pipeline { grid-template-columns:1fr; padding:1rem; }.pipeline-stage { min-height:150px; }.model-diagram,.explain-grid,.benchmark-layout { grid-template-columns:1fr; }.intelligence-diagram { grid-template-columns:1fr; padding:1rem; }.int-arrow { display:block; transform:rotate(90deg); text-align:center; }.clinical-flow { grid-template-columns:1fr; padding:1rem; }.flow-arrow { display:block; text-align:center; transform:none; }
  .benchmark-layout { padding:1rem; }.bar-row { grid-template-columns:76px 1fr 48px; }.research-boundary,.evidence-callout { margin-left:1rem; margin-right:1rem; }.references { padding-left:1rem; padding-right:1rem; }.about-footer { flex-direction:column; align-items:flex-start; }.about-footer p { text-align:left; }.about-footer > a { white-space:normal; }
}

@media (max-width: 430px) {
  .hero-visual { min-height:390px; }.signal-center { width:205px; }.floating-node small { display:none; }.floating-node { min-width:70px; }.hero-actions a { width:100%; }.hero-trust-row { margin-top:1.5rem; }.task-visual { height:105px; }.section-card { border-radius:1.15rem; }.hero-shell { border-radius:1.15rem; }.bar-row { grid-template-columns:64px 1fr 44px; gap:.4rem; }.bar-row > span,.bar-row b { font-size:.62rem; }
}

@media (prefers-reduced-motion: reduce) {
  *,*::before,*::after { scroll-behavior:auto !important; transition:none !important; }
}
</style>