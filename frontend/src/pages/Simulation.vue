<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

// --- Parameters ---
const magnitude = ref(2.5);
const frequency = ref(1.5);
const duration = ref(10);

// --- State ---
const chartCanvas = ref(null);
let chart = null;
let animId = null;

// The "Buffer" holds the full simulation data from Python
let playbackBuffer = []; 
let playbackCursor = 0; 

// The "Live Data" is what is currently shown on screen
const maxPoints = 300; // How many points to keep on screen (window width)
const liveLabels = new Array(maxPoints).fill('');
const liveData = new Array(maxPoints).fill(0);

// Stats
const stats = ref([
  { l: 'Max Disp', v: '0.00' },
  { l: 'Buffer', v: '0%' },
  { l: 'Status', v: 'Idle' }
]);

// Physics Computations
const physicsStats = ref([
  { l: 'Amplitude', v: '0.00' },
  { l: 'Energy', v: '0.00' },
  { l: 'P-Wave Freq', v: '0.0' },
  { l: 'S-Wave Freq', v: '0.0' },
  { l: 'Surface Freq', v: '0.0' },
  { l: 'Max Disp (Calc)', v: '0.00' }
]);

let debounceTimer = null;

// --- Chart Initialization ---
// Initialize chart
const initChart = () => {
  if (!chartCanvas.value) return;
  const ctx = chartCanvas.value.getContext('2d');
  
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: liveLabels,
      datasets: [{
        data: liveData,
        borderColor: '#10b981',
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
        tension: 0.1,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      interaction: { mode: 'nearest', intersect: false },
      scales: {
        x: { display: false },
        y: {
          display: true,
          // 👇 CHANGED: Removed fixed min/max
          // suggestedMin/Max keeps the graph from zooming in too much on tiny noise
          suggestedMin: -10,
          suggestedMax: 10,
          // grace adds 20% empty space at the top/bottom so the line never hits the edge
          grace: '20%', 
          grid: { color: 'rgba(16,185,129,0.1)' },
          // 👇 OPTIONAL: Turn ticks ON if you want to see the numbers change
          ticks: { display: true, color: '#64748b', font: { size: 10 } } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    }
  });
};

// --- API Fetcher ---
const fetchSimulation = async () => {
  stats.value[2].v = 'Simulating...';
  
  try {
    const response = await fetch('http://127.0.0.1:8000/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        magnitude: magnitude.value,
        frequency: frequency.value,
        duration: duration.value
      }),
    });

    if (!response.ok) throw new Error('Network error');

    const data = await response.json();
    
    // LOAD THE BUFFER:
    // We overwrite the buffer with the new earthquake event
    playbackBuffer = data.waveform;
    playbackCursor = 0; // Start playing from the beginning of the new wave
    
    // Compute max displacement from buffer (for verification against backend)
    const maxDisp = playbackBuffer.reduce((max, val) => Math.max(max, Math.abs(val)), 0).toFixed(2);
    stats.value[0].v = maxDisp;
    
    // Update physics stats from backend computations
    physicsStats.value[0].v = data.amplitude.toFixed(2);
    physicsStats.value[1].v = data.energy.toExponential(2);
    physicsStats.value[2].v = data.p_wave_freq.toFixed(1);
    physicsStats.value[3].v = data.s_wave_freq.toFixed(1);
    physicsStats.value[4].v = data.surface_wave_freq.toFixed(1);
    physicsStats.value[5].v = data.max_displacement.toFixed(2);
    
    stats.value[2].v = 'Streaming';

  } catch (error) {
    console.error("Simulation error:", error);
    stats.value[2].v = 'Error';
  }
};

// --- The Live Loop ---
const tick = () => {
  // 1. Get the next value
  let nextValue = 0;

  if (playbackCursor < playbackBuffer.length) {
    // We are playing the earthquake event from the backend
    nextValue = playbackBuffer[playbackCursor];
    playbackCursor++;
    
    // Update stats progress
    const progress = Math.round((playbackCursor / playbackBuffer.length) * 100);
    stats.value[1].v = `${progress}%`;
  } else {
    // Buffer empty: Generate tiny background noise so the graph doesn't look "dead"
    stats.value[2].v = 'Waiting';
    nextValue = (Math.random() - 0.5) * 0.1; 
  }

  // 2. Shift the live arrays (Queue behavior)
  liveData.shift(); // Remove oldest
  liveData.push(nextValue); // Add newest

  // 3. Render
  if (chart) {
    chart.update('none'); // 'none' mode is crucial for high performance
  }

  animId = requestAnimationFrame(tick);
};

// --- Watchers ---
watch([magnitude, frequency, duration], () => {
  // When slider moves, we prepare to fetch new physics data
  // The graph keeps scrolling (tick is running), but we update the source
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchSimulation();
  }, 300); // 300ms delay to feel responsive but safe
});

const resetSimulation = () => {
  magnitude.value = 2.5;
  frequency.value = 1.5;
  duration.value = 10;
  // This triggers the watcher -> fetchSimulation
};

// --- Lifecycle ---
onMounted(() => {
  initChart();
  fetchSimulation(); // Get initial data
  animId = requestAnimationFrame(tick); // Start the live loop
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

              <v-btn
                block
                class="mt-8 reset-btn"
                @click="resetSimulation"
              >
                Trigger New Event
              </v-btn>
            </v-card>
          </v-col>

          <v-col cols="12" md="9">
            <v-card
              variant="outlined"
              class="pa-4 border-slate-800 bg-slate-900/40 rounded-xl h-[400px] relative overflow-hidden"
            >
              <canvas ref="chartCanvas"></canvas>
            </v-card>

            <v-row class="mt-4">
              <v-col v-for="s in stats" :key="s.l" cols="4">
                <v-card variant="outlined" class="pa-4 border-slate-800 bg-slate-900/40 rounded-lg text-center">
                  <div class="text-[9px] text-slate-500 uppercase font-bold tracking-[0.3em] mb-1">{{ s.l }}</div>
                  <div class="font-mono text-xl text-emerald-400/80">{{ s.v }}</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- New Physics Computations Section -->
            <v-row class="mt-4">
              <v-col v-for="p in physicsStats" :key="p.l" cols="4" md="2">
                <v-card variant="outlined" class="pa-4 border-slate-800 bg-slate-900/40 rounded-lg text-center">
                  <div class="text-[9px] text-slate-500 uppercase font-bold tracking-[0.3em] mb-1">{{ p.l }}</div>
                  <div class="font-mono text-xl text-emerald-400/80">{{ p.v }}</div>
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
/* existing styles */
.bg-slate-950 { background-color: #020617; }
.bg-slate-900\/40 { background-color: rgba(15,23,42,0.4); }

.border-slate-800 {
  border-color: #10b981 !important;
  box-shadow:
    0 0 6px rgba(16,185,129,0.35),
    0 0 18px rgba(16,185,129,0.25),
    inset 0 0 6px rgba(16,185,129,0.15);
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}

.reset-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ecfdf5;
  border: 1px solid rgba(16, 185, 129, 0.6);
  box-shadow:
    0 0 10px rgba(16, 185, 129, 0.35),
    inset 0 0 6px rgba(16, 185, 129, 0.25);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    background 0.25s ease;
}

.reset-btn:hover {
  transform: translateY(-2px) scale(1.03);
  background: linear-gradient(135deg, #34d399, #10b981);
  box-shadow:
    0 0 18px rgba(16, 185, 129, 0.7),
    0 0 35px rgba(16, 185, 129, 0.4),
    inset 0 0 10px rgba(16, 185, 129, 0.35);
}

.reset-btn:active {
  transform: scale(0.98);
}

.border-slate-800:hover {
  box-shadow:
    0 0 14px rgba(16, 185, 129, 0.7),
    0 0 35px rgba(16, 185, 129, 0.45),
    0 0 60px rgba(16, 185, 129, 0.25),
    inset 0 0 12px rgba(16, 185, 129, 0.35);
  transform: translateY(-2px);
}
</style>