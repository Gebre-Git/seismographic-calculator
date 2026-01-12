<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

// Simulation parameters
const magnitude = ref(2.5);
const frequency = ref(1.5);
const duration = ref(10);

// Chart and canvas refs
const chartCanvas = ref(null);
let chart = null;
let animId = null;
let lastTime = Date.now() / 1000;
let phase = 0;

// Points array for plotting
const points = ref([]);

// Stats (optional minimal info for left panel)
const stats = ref([
  { l: 'Max Amp', v: 0 },
  { l: 'Buffer', v: 0 },
  { l: 'Stability', v: '99.9%' }
]);

// Initialize chart
const initChart = () => {
  if (!chartCanvas.value) return;
  const ctx = chartCanvas.value.getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        data: [],
        borderColor: '#10b981',
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
        tension: 0.35
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 0 },
      scales: {
        x: { display: false },
        y: {
          display: true,
          min: -15,
          max: 15,
          grid: { color: 'rgba(16,185,129,0.1)' },
          ticks: { display: false }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    }
  });
};

// Tick function for live plotting
const tick = () => {
  const now = Date.now() / 1000;
  const dt = now - lastTime;
  lastTime = now;

  phase += dt * frequency.value * 2 * Math.PI;
  const wave = Math.sin(phase);
  const jitter = (Math.random() - 0.5) * 0.4;
  const val = (wave + jitter) * magnitude.value;

  points.value.push({ x: now, y: val });

  const cut = now - duration.value;
  points.value = points.value.filter(p => p.x > cut);

  if (chart) {
    chart.data.labels = points.value.map(p => '');
    chart.data.datasets[0].data = points.value.map(p => p.y);
    chart.update('none');
  }

  // Update stats
  stats.value[0].v = Math.max(...points.value.map(p => Math.abs(p.y))).toFixed(2);
  stats.value[1].v = `${points.value.length} pts`;

  animId = requestAnimationFrame(tick);
};

// Reset function with animation
const resetSimulation = () => {
  // Animate points fade-out from top
  if (points.value.length) {
    const fadeOut = setInterval(() => {
      points.value = points.value.slice(0, Math.floor(points.value.length * 0.8));
      if (points.value.length === 0) clearInterval(fadeOut);
    }, 30);
  }

  // Reset sliders after fade-out
  setTimeout(() => {
    magnitude.value = 2.5;
    frequency.value = 1.5;
    duration.value = 10;
    points.value = [];
    if (chart) {
      chart.data.labels = [];
      chart.data.datasets[0].data = [];
      chart.update();
    }
  }, 300);
};

watch([magnitude, frequency, duration], () => {
  // Real-time adjustments applied automatically
});

onMounted(() => {
  initChart();
  animId = requestAnimationFrame(tick);
});

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId);
});
</script>

<template>
  <v-app theme="dark">
    <v-main class="bg-slate-950">
      <v-container fluid class="pa-6">
        <v-row>
          <!-- Controls Panel -->
          <v-col cols="12" md="3">
            <v-card variant="outlined" class="pa-6 border-slate-800 bg-slate-900/40 rounded-xl backdrop-blur-sm">
              <div class="mb-6">
                <div class="d-flex justify-space-between align-center mb-2">
                  <label class="text-xs font-bold text-slate-400 uppercase tracking-widest">Magnitude</label>
                  <span class="text-emerald-400 font-mono text-lg">{{ magnitude.toFixed(1) }}</span>
                </div>
                <v-slider
                  v-model="magnitude"
                  min="0"
                  max="10"
                  step="0.1"
                  color="green"
                  hide-details
                  thumb-color="green"
                  track-color="rgba(16,185,129,0.3)"
                ></v-slider>
              </div>

              <div class="mb-6">
                <div class="d-flex justify-space-between align-center mb-2">
                  <label class="text-xs font-bold text-slate-400 uppercase tracking-widest">Frequency</label>
                  <span class="text-emerald-400 font-mono text-lg">{{ frequency.toFixed(1) }}</span>
                </div>
                <v-slider
                  v-model="frequency"
                  min="0.1"
                  max="5"
                  step="0.1"
                  color="green"
                  hide-details
                  thumb-color="green"
                  track-color="rgba(16,185,129,0.3)"
                ></v-slider>
              </div>

              <div class="mb-6">
                <div class="d-flex justify-space-between align-center mb-2">
                  <label class="text-xs font-bold text-slate-400 uppercase tracking-widest">Duration</label>
                  <span class="text-emerald-400 font-mono text-lg">{{ duration }}s</span>
                </div>
                <v-slider
                  v-model="duration"
                  min="5"
                  max="30"
                  step="1"
                  color="green"
                  hide-details
                  thumb-color="green"
                  track-color="rgba(16,185,129,0.3)"
                ></v-slider>
              </div>

              <!-- Reset Button -->
              <v-btn
                block
                class="mt-8 reset-btn"
                @click="resetSimulation"
              >
                Reset
              </v-btn>
            </v-card>
          </v-col>

          <!-- Graph Area -->
          <v-col cols="12" md="9">
            <v-card
              variant="outlined"
              class="pa-4 border-slate-800 bg-slate-900/40 rounded-xl h-[400px] relative overflow-hidden"
            >
              <canvas ref="chartCanvas"></canvas>
            </v-card>

            <!-- Minimal Stats -->
            <v-row class="mt-4">
              <v-col v-for="s in stats" :key="s.l" cols="4">
                <v-card variant="outlined" class="pa-4 border-slate-800 bg-slate-900/40 rounded-lg text-center">
                  <div class="text-[9px] text-slate-500 uppercase font-bold tracking-[0.3em] mb-1">{{ s.l }}</div>
                  <div class="font-mono text-xl text-emerald-400/80">{{ s.v }}</div>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.bg-slate-950 { background-color: #020617; }
.bg-slate-900\/40 { background-color: rgba(15,23,42,0.4); }
.border-slate-800 { border-color: #1e293b !important; }

/* Reset Button Styling */
.reset-btn {
  background-color: #10b981;
  color: white;
  font-weight: bold;
  transition: transform 0.2s, background-color 0.3s;
}
.reset-btn:hover {
  background-color: #059669;
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(16,185,129,0.6);
}
</style>
