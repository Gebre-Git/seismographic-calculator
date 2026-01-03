
<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";

// Core simulation parameters (Preserved names)
const magnitude = ref(5);
const duration = ref(10);
const frequent = ref(2);

// UI state
const isLoading = ref(false);
const isLiveSimulating = ref(false);

// Canvas refs (Preserved names)
const historicalCanvas = ref(null);
const liveCanvas = ref(null);
const fftCanvas = ref(null);

// Chart instances (Preserved names)
let historicalChart = null;
let liveChart = null;
let fftChart = null;
let intervalId = null;

onMounted(() => {
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    elements: { point: { radius: 0 } },
    plugins: {
      legend: { display: false }
    },
    scales: { 
      x: { display: false }, 
      y: { 
        suggestedMin: -10, 
        suggestedMax: 10,
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { color: '#71717a' }
      } 
    }
  };

  historicalChart = new Chart(historicalCanvas.value.getContext('2d'), {
    type: "line",
    data: { 
      labels: [], 
      datasets: [{ 
        label: "Static Analysis", 
        data: [], 
        borderColor: "#3b82f6", 
        borderWidth: 1.5,
        fill: true,
        backgroundColor: 'rgba(59, 130, 246, 0.05)'
      }] 
    },
    options: commonOptions
  });

  liveChart = new Chart(liveCanvas.value.getContext('2d'), {
    type: "line",
    data: { 
      labels: [], 
      datasets: [{ 
        label: "Live Feed", 
        data: [], 
        borderColor: "#10b981", 
        borderWidth: 2,
        backgroundColor: 'rgba(16, 185, 129, 0.1)'
      }] 
    },
    options: { ...commonOptions, animation: false }
  });

  fftChart = new Chart(fftCanvas.value.getContext("2d"), {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Frequency Spectrum (FFT)",
        data: [],
        borderColor: "#ef4444",
        borderWidth: 1.5,
        fill: true,
        backgroundColor: 'rgba(239, 68, 68, 0.1)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: { point: { radius: 0 } },
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { 
          title: { display: true, text: "Frequency (Hz)", color: '#71717a' },
          grid: { display: false },
          ticks: { color: '#71717a' }
        },
        y: { 
          title: { display: true, text: "Amplitude", color: '#71717a' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#71717a' }
        }
      }
    }
  });
});

async function simulate() {
  if (intervalId) clearInterval(intervalId);
  isLoading.value = true;
  isLiveSimulating.value = false;

  try {
    const response = await axios.post("http://127.0.0.1:8000/simulate", {
      magnitude: magnitude.value,
      duration: duration.value,
      frequency: frequent.value
    });

    const { time, waveform, frequency, spectrum } = response.data;

    historicalChart.data.labels = time;
    historicalChart.data.datasets[0].data = waveform;
    historicalChart.update();

    fftChart.data.labels = frequency;
    fftChart.data.datasets[0].data = spectrum;
    fftChart.update();

    liveChart.data.labels = [];
    liveChart.data.datasets[0].data = [];
    let currentIndex = 0;

    isLiveSimulating.value = true;
    intervalId = setInterval(() => {
      if (currentIndex < waveform.length) {
        liveChart.data.labels.push("");
        liveChart.data.datasets[0].data.push(waveform[currentIndex]);

        if (liveChart.data.datasets[0].data.length > 80) {
          liveChart.data.labels.shift();
          liveChart.data.datasets[0].data.shift();
        }

        liveChart.update('none');
        currentIndex++;
      } else {
        clearInterval(intervalId);
        isLiveSimulating.value = false;
      }
    }, 15);

  } catch (error) {
    console.error("Simulation error", error);
  } finally {
    isLoading.value = false;
  }
}

onBeforeUnmount(() => { if (intervalId) clearInterval(intervalId); });
</script>

<template>
  <v-container fluid class="bg-zinc-950 min-h-screen pa-6 lg:pa-10">
    <v-row>
      <!-- Controls Sidebar -->
      <v-col cols="12" md="4" lg="3">
        <v-card class="bg-zinc-900 border border-zinc-800 rounded-xl pa-6 shadow-2xl sticky-sidebar">
          <div class="mb-8">
            <h1 class="text-h4 font-weight-black text-white">
              Seismo<span class="text-blue-lighten-1">Suite</span>
            </h1>
            <p class="text-caption text-zinc-500 mt-1 uppercase font-weight-bold tracking-widest">
              Digital Seismograph Engine
            </p>
          </div>

          <v-divider class="mb-8 border-zinc-800"></v-divider>

          <!-- Inputs -->
          <div class="space-y-10">
            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Duration</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ duration }}s
                </v-chip>
              </div>
              <v-slider
                v-model="duration"
                min="1"
                max="60"
                step="1"
                hide-details
                color="blue-darken-1"
                track-color="zinc-800"
              ></v-slider>
              <p class="text-[10px] text-zinc-500 italic mt-2">Total time window for analysis.</p>
            </div>

            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Magnitude</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ magnitude }} Mw
                </v-chip>
              </div>
              <v-slider
                v-model="magnitude"
                min="1"
                max="10"
                step="0.1"
                hide-details
                color="emerald-darken-1"
                track-color="zinc-800"
              ></v-slider>
              <p class="text-[10px] text-zinc-500 italic mt-2">Maximum wave amplitude amplitude.</p>
            </div>

            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Frequency</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ frequent }} Hz
                </v-chip>
              </div>
              <v-slider
                v-model="frequent"
                min="0.1"
                max="20"
                step="0.1"
                hide-details
                color="red-darken-1"
                track-color="zinc-800"
              ></v-slider>
              <p class="text-[10px] text-zinc-500 italic mt-2">Dominant frequency of seismic oscillations.</p>
            </div>

            <v-btn
              block
              size="x-large"
              color="blue-darken-2"
              class="rounded-lg font-weight-bold text-uppercase mt-8"
              @click="simulate"
              :loading="isLoading"
              :disabled="isLoading || isLiveSimulating"
              elevation="6"
            >
              <template v-slot:loader>
                <v-progress-circular indeterminate size="20"></v-progress-circular>
              </template>
              Run Simulation
            </v-btn>
          </div>

          <!-- Status Indicator -->
          <div class="mt-12 pa-4 bg-zinc-950/50 border border-zinc-800 rounded-lg">
            <h4 class="text-overline font-weight-black text-zinc-600 mb-2">Sensor Network</h4>
            <div class="d-flex justify-space-between text-caption mb-1">
              <span class="text-zinc-500">Node Cluster</span>
              <span class="text-emerald-darken-1 font-weight-bold">ACTIVE</span>
            </div>
            <div class="d-flex justify-space-between text-caption">
              <span class="text-zinc-500">Latency</span>
              <span class="text-blue-darken-1 font-mono">12ms</span>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Charts Area -->
      <v-col cols="12" md="8" lg="9">
        <v-row>
          <!-- Waveform Split -->
          <v-col cols="12" lg="6">
            <v-card class="bg-zinc-900 border border-zinc-800 rounded-xl pa-5 h-100 relative overflow-hidden chart-wrapper shadow-lg">
              <div class="accent-bar bg-blue-darken-1"></div>
              <div class="d-flex justify-space-between align-center mb-4">
                <div>
                  <h3 class="text-subtitle-1 font-weight-bold text-zinc-100">Historical Waveform</h3>
                  <p class="text-caption text-zinc-500">Full dataset rendering for structural analysis.</p>
                </div>
                <v-icon v-if="isLoading" color="blue" size="small" class="mdi-spin">mdi-loading</v-icon>
              </div>
              <div class="canvas-container">
                <canvas ref="historicalCanvas"></canvas>
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" lg="6">
            <v-card class="bg-zinc-900 border border-zinc-800 rounded-xl pa-5 h-100 relative overflow-hidden chart-wrapper shadow-lg">
              <div class="accent-bar bg-emerald-darken-1"></div>
              <div class="d-flex justify-space-between align-center mb-4">
                <div>
                  <h3 class="text-subtitle-1 font-weight-bold text-zinc-100">Real-Time Seismograph</h3>
                  <p class="text-caption text-zinc-500">Simulated sensor telemetry from the epicenter.</p>
                </div>
                <div v-if="isLiveSimulating" class="live-tag">
                  <span class="pulse-dot"></span>
                  <span class="text-caption font-weight-black text-emerald">LIVE</span>
                </div>
              </div>
              <div class="canvas-container">
                <canvas ref="liveCanvas"></canvas>
              </div>
            </v-card>
          </v-col>

          <!-- FFT Analysis -->
          <v-col cols="12">
            <v-card class="bg-zinc-900 border border-zinc-800 rounded-xl pa-5 relative overflow-hidden chart-wrapper shadow-lg">
              <div class="accent-bar bg-red-darken-1"></div>
              <div class="mb-4">
                <h3 class="text-subtitle-1 font-weight-bold text-zinc-100">Frequency Spectrum (FFT)</h3>
                <p class="text-caption text-zinc-500">Frequency-domain distribution of seismic energy.</p>
              </div>
              <div class="canvas-container fft-size">
                <canvas ref="fftCanvas"></canvas>
              </div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Dynamic Metrics -->
        <v-row class="mt-4">
          <v-col cols="6" sm="3">
            <div class="bg-zinc-900/40 border border-zinc-800 rounded-xl pa-4 text-center">
              <p class="text-overline text-zinc-600 font-weight-black mb-1">Peak Amplitude</p>
              <p class="text-h6 font-mono text-zinc-100">{{ (magnitude * 1.1).toFixed(2) }}</p>
            </div>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="bg-zinc-900/40 border border-zinc-800 rounded-xl pa-4 text-center">
              <p class="text-overline text-zinc-600 font-weight-black mb-1">Dominant Peak</p>
              <p class="text-h6 font-mono text-zinc-100">{{ frequent.toFixed(2) }} Hz</p>
            </div>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="bg-zinc-900/40 border border-zinc-800 rounded-xl pa-4 text-center">
              <p class="text-overline text-zinc-600 font-weight-black mb-1">Time Slice</p>
              <p class="text-h6 font-mono text-zinc-100">{{ duration }}s</p>
            </div>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="bg-zinc-900/40 border border-zinc-800 rounded-xl pa-4 text-center">
              <p class="text-overline text-zinc-600 font-weight-black mb-1">Energy Ratio</p>
              <p class="text-h6 font-mono text-zinc-100">{{ (magnitude * 0.85).toFixed(1) }}σ</p>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.bg-zinc-950 { background-color: #09090b; }
.bg-zinc-900 { background-color: #18181b; }
.bg-zinc-900\/40 { background-color: rgba(24, 24, 27, 0.4); }
.bg-zinc-950\/50 { background-color: rgba(9, 9, 11, 0.5); }
.border-zinc-800 { border-color: #27272a !important; }
.text-zinc-100 { color: #f4f4f5; }
.text-zinc-300 { color: #d4d4d8; }
.text-zinc-400 { color: #a1a1aa; }
.text-zinc-500 { color: #71717a; }
.text-zinc-600 { color: #52525b; }

.sticky-sidebar {
  position: sticky;
  top: 2rem;
}

.chart-wrapper {
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.chart-wrapper:hover {
  border-color: #3f3f46 !important;
}

.canvas-container {
  height: 280px;
  width: 100%;
}

.fft-size {
  height: 350px;
}

.accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
}

.space-y-10 > * + * {
  margin-top: 2.5rem;
}

.space-y-8 > * + * {
  margin-top: 2rem;
}

.live-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(16, 185, 129, 0.1);
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  animation: pulse-animation 1.5s infinite;
}

@keyframes pulse-animation {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

:deep(.v-slider-thumb) {
  border: 2px solid white;
}

:deep(.v-btn__content) {
  letter-spacing: 0.1em;
}

.mdi-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
