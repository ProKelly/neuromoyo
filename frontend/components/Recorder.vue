<!--
  MediaRecorder wrapper with a LIVE waveform during recording, drawn from the real
  input signal via Web Audio's AnalyserNode -- this is functional feedback (the
  health worker can see the mic is actually picking up voice), not decoration.
  Emits `recorded` with the captured Blob once recording stops.
-->
<template>
  <div class="flex flex-col gap-4">
    <div class="relative rounded-2xl bg-teal-900/95 h-28 overflow-hidden flex items-center justify-center px-4">
      <canvas ref="canvasEl" class="w-full h-16" width="600" height="120" />
      <span v-if="!recording && !audioUrl" class="absolute text-teal-100/70 text-sm">
        Waveform appears here while recording
      </span>
    </div>

    <div class="flex items-center gap-3">
      <button
        v-if="!recording && !audioUrl"
        class="inline-flex items-center gap-2 rounded-full bg-teal-600 hover:bg-teal-700 text-white px-5 py-2.5 text-sm font-semibold shadow-sm transition-colors cursor-pointer"
        @click="start"
      >
        <span class="w-2 h-2 rounded-full bg-white"></span>
        Start recording
      </button>

      <button
        v-if="recording"
        class="inline-flex items-center gap-2 rounded-full bg-rust-600 hover:bg-rust-700 text-white px-5 py-2.5 text-sm font-semibold shadow-sm transition-colors cursor-pointer"
        @click="stop"
      >
        <span class="w-2.5 h-2.5 rounded-sm bg-white"></span>
        Stop · {{ elapsed }}s
      </button>

      <template v-if="audioUrl">
        <audio :src="audioUrl" controls class="h-9 flex-1 min-w-0" />
        <button
          class="rounded-full border border-mist bg-white px-4 py-2 text-sm font-medium text-ink-soft hover:bg-mist transition-colors cursor-pointer"
          @click="reset"
        >
          Re-record
        </button>
      </template>
    </div>

    <p v-if="error" class="text-sm text-rust-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ recorded: [blob: Blob] }>()

const recording = ref(false)
const audioUrl = ref<string | null>(null)
const error = ref<string | null>(null)
const elapsed = ref(0)
const canvasEl = ref<HTMLCanvasElement | null>(null)

let mediaRecorder: MediaRecorder | null = null
let chunks: Blob[] = []
let stream: MediaStream | null = null
let timer: ReturnType<typeof setInterval> | null = null
let audioCtx: AudioContext | null = null
let analyser: AnalyserNode | null = null
let rafId: number | null = null

async function start() {
  error.value = null
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    chunks = []
    mediaRecorder = new MediaRecorder(stream)
    mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data) }
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/webm' })
      audioUrl.value = URL.createObjectURL(blob)
      emit('recorded', blob)
      stream?.getTracks().forEach((t) => t.stop())
      stopWaveform()
    }
    mediaRecorder.start()
    recording.value = true
    elapsed.value = 0
    timer = setInterval(() => { elapsed.value += 1 }, 1000)
    startWaveform(stream)
  } catch (e) {
    error.value = 'Could not access the microphone. Check permissions and try again.'
  }
}

function stop() {
  mediaRecorder?.stop()
  recording.value = false
  if (timer) clearInterval(timer)
}

function reset() {
  audioUrl.value = null
  chunks = []
}

function startWaveform(mediaStream: MediaStream) {
  audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)()
  const source = audioCtx.createMediaStreamSource(mediaStream)
  analyser = audioCtx.createAnalyser()
  analyser.fftSize = 256
  source.connect(analyser)
  drawWaveform()
}

function drawWaveform() {
  const canvas = canvasEl.value
  if (!canvas || !analyser) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  const bufferLength = analyser.frequencyBinCount
  const data = new Uint8Array(bufferLength)

  const render = () => {
    if (!analyser) return
    analyser.getByteFrequencyData(data)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    const barCount = 40
    const step = Math.floor(bufferLength / barCount)
    const barWidth = canvas.width / barCount
    for (let i = 0; i < barCount; i++) {
      const v = data[i * step] / 255
      const barHeight = Math.max(4, v * canvas.height * 0.9)
      const x = i * barWidth
      const y = (canvas.height - barHeight) / 2
      ctx.fillStyle = '#cfe8de'
      ctx.fillRect(x + barWidth * 0.25, y, barWidth * 0.5, barHeight)
    }
    rafId = requestAnimationFrame(render)
  }
  render()
}

function stopWaveform() {
  if (rafId) cancelAnimationFrame(rafId)
  rafId = null
  analyser = null
  audioCtx?.close()
  audioCtx = null
}

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
  stream?.getTracks().forEach((t) => t.stop())
  stopWaveform()
})
</script>
