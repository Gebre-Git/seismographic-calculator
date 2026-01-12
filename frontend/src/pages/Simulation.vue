<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import Chart from "chart.js/auto";

// Simulation parameters
const magnitude = ref(5);
const duration = ref(10);
const frequency = ref(2);

// Canvas ref
const chartCanvas = ref(null);
let liveChart = null;
let intervalId = null;

// Real-time points
let waveform = [];

// Initialize Chart.js
const initChart = () => {
  if (!chartCanvas.value) return;
  const ctx = chartCanvas.value.getContext("2d");
  liveChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          data: [],
          borderColor: "#10b981",
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0.35,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: { display: false },
        y: {
          min: -15,
          max: 15,
          grid: { color: "rgba(255, 255, 255, 0.02)" },
          ticks: { display: false },
        },
      },
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
    },
  });
};

// Fetch simulation data from backend
const fetchSimulation = async () => {
  try {
    const res = await axios.post("http://127.0.0.1:8000/simulate", {
      magnitude: magnitude.value,
      duration: duration.value,
      frequency: frequency.value,
    });
    waveform = res.data.waveform || [];
    startLiveUpdate();
  } catch (err) {
    console.error("Simulation error", err);
  }
};

// Update chart in real-time
const startLiveUpdate = () => {
  if (intervalId) clearInterval(intervalId);
  let index = 0;
  liveChart.data.labels = [];
  liveChart.data.datasets[0].data = [];

  intervalId = setInterval(() => {
    if (index < waveform.length) {
      liveChart.data.labels.push("");
      liveChart.data.datasets[0].data.push(waveform[index]);
      if (liveChart.data.datasets[0].data.length > 80) {
        liveChart.data.labels.shift();
        liveChart.data.datasets[0].data.shift();
      }
      liveChart.update("none");
      index++;
    } else {
      clearInterval(intervalId);
    }
  }, 15);
};

// Update simulation whenever sliders change
watch([magnitude, duration, frequency], fetchSimulation);

onMounted(() => {
  initChart();
  fetchSimulation();
});

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId);
});
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

          <!-- Sliders -->
          <div class="space-y-10">
            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Duration</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ duration }}s
                </v-chip>
              </div>
              <v-slider v-model="duration" min="1" max="60" step="1" hide-details color="blue-darken-1" track-color="zinc-800"></v-slider>
            </div>

            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Magnitude</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ magnitude }} Mw
                </v-chip>
              </div>
              <v-slider v-model="magnitude" min="1" max="10" step="0.1" hide-details color="emerald-darken-1" track-color="zinc-800"></v-slider>
            </div>

            <div class="control-group">
              <div class="d-flex justify-space-between align-center mb-2">
                <label class="text-subtitle-2 text-zinc-300 font-weight-medium">Frequency</label>
                <v-chip size="small" variant="flat" color="zinc-800" class="text-zinc-100 font-mono">
                  {{ frequency }} Hz
                </v-chip>
              </div>
              <v-slider v-model="frequency" min="0.1" max="20" step="0.1" hide-details color="red-darken-1" track-color="zinc-800"></v-slider>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Graph Area -->
      <v-col cols="12" md="8" lg="9">
        <v-card class="bg-zinc-900 border border-zinc-800 rounded-xl pa-5 h-100 shadow-lg">
          <canvas ref="chartCanvas"></canvas>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.bg-zinc-950 { background-color: #09090b; }
.bg-zinc-900 { background-color: #18181b; }
.border-zinc-800 { border-color: #27272a !important; }
.text-zinc-100 { color: #f4f4f5; }
.text-zinc-300 { color: #d4d4d8; }
.text-zinc-500 { color: #71717a; }

.sticky-sidebar { position: sticky; top: 2rem; }
.space-y-10 > * + * { margin-top: 2.5rem; }
</style>
